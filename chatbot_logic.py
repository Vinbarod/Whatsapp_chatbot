import sqlite3
from typing import Annotated
from typing_extensions import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.sqlite import SqliteSaver

from api_services import (
    get_all_products,
    get_product_details,
    track_order_status,
    get_pricing_plans,
    get_active_offers
)

class State(TypedDict):
    messages: Annotated[list, add_messages]

def _extract_text(content):
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        texts = []
        for item in content:
            if isinstance(item, dict) and 'text' in item:
                texts.append(item['text'])
            elif isinstance(item, str):
                texts.append(item)
        return " ".join(texts)
    return str(content)

class ChatbotLogic:
    def __init__(self, api_key: str):

        self.tools = [
            get_all_products,
            get_product_details,
            track_order_status,
            get_pricing_plans,
            get_active_offers
        ]

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key
        )

        self.llm_with_tools = self.llm.bind_tools(self.tools)

        graph_builder = StateGraph(State)

        
        def chatbot(state: State):
            sys_msg = SystemMessage(content="""
You are a friendly WhatsApp-style AI Sales Assistant for an electronics store called GadgetKart 🛍️

Behavior:
- Talk like a real sales assistant (friendly, short, helpful)
- Use light emojis 😊
- Keep responses under 4–6 lines

Menu Handling:
If user says "menu", "start", or "help", show:

📌 *Main Menu*:
1️⃣ View Products  
2️⃣ Check Price  
3️⃣ Track Order  
4️⃣ Active Offers  
5️⃣ Talk to Support  

Capabilities:
- Use tools to fetch product details, pricing, orders, and offers
- Suggest products when user is confused
- Explain clearly (name, price, key benefit)

Goal:
Help user quickly find and buy electronics ⚡
""")

            response = self.llm_with_tools.invoke([sys_msg] + state["messages"])
            return {"messages": [response]}

        graph_builder.add_node("chatbot", chatbot)

        tool_node = ToolNode(tools=self.tools)
        graph_builder.add_node("tools", tool_node)

        graph_builder.add_conditional_edges("chatbot", tools_condition)
        graph_builder.add_edge("tools", "chatbot")
        graph_builder.add_edge(START, "chatbot")

       
        self.conn = sqlite3.connect("chat_history.db", check_same_thread=False)
        self.memory = SqliteSaver(self.conn)

        self.graph = graph_builder.compile(checkpointer=self.memory)

    def process_query(self, user_query: str, session_id: str):

        if user_query.lower() in ["menu", "start", "help"]:
            return """📌 *Main Menu*:
1️⃣ View Products  
2️⃣ Check Price  
3️⃣ Track Order  
4️⃣ Active Offers  
5️⃣ Talk to Support  

👉 What would you like to do?"""

        config = {"configurable": {"thread_id": session_id}}

        events = self.graph.stream(
            {"messages": [HumanMessage(content=user_query)]},
            config,
            stream_mode="values"
        )

        final_response = None
        for event in events:
            final_response = event["messages"][-1]

        return _extract_text(final_response.content)

    def get_chat_history_for_display(self, session_id: str):
        config = {"configurable": {"thread_id": session_id}}
        try:
            state = self.graph.get_state(config)
            if not state or not state.values:
                return []

            messages = state.values.get("messages", [])
            display_msgs = []

            for msg in messages:
                if isinstance(msg, HumanMessage):
                    display_msgs.append({
                        "role": "user",
                        "content": _extract_text(msg.content)
                    })
                elif msg.type == "ai" and msg.content:
                    display_msgs.append({
                        "role": "assistant",
                        "content": _extract_text(msg.content)
                    })

            return display_msgs
        except Exception:
            return []
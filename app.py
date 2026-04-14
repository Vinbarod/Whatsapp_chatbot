import streamlit as st
import os
import uuid
from dotenv import load_dotenv
from chatbot_logic import ChatbotLogic


load_dotenv()

st.set_page_config(page_title="AI Sales Agent", layout="centered")


st.markdown("""
<style>

/* Background */
body, .stApp {
    background: linear-gradient(to bottom, #f9fcff, #e3f2fd);
}

/* Floating bubbles container */
.bubbles {
    position: fixed;
    width: 100%;
    height: 100%;
    z-index: -1;
    top: 0;
    left: 0;
}

/* Bubble style */
.bubble {
    position: absolute;
    bottom: -50px;
    background: rgba(0, 150, 255, 0.1);
    border-radius: 50%;
    animation: floatUp linear infinite;
}

/* Animation */
@keyframes floatUp {
    0% {
        transform: translateY(0) scale(1);
        opacity: 0.5;
    }
    100% {
        transform: translateY(-100vh) scale(1.5);
        opacity: 0;
    }
}

/* Chat container */
.chat-container {
    max-width: 700px;
    margin: auto;
    padding-bottom: 80px;
}

/* User message */
.user-msg {
    background-color: #0078ff;
    color: white;
    padding: 10px 14px;
    border-radius: 12px;
    margin: 8px 0;
    text-align: right;
}

/* Bot message */
.bot-msg {
    background-color: #ffffff;
    color: #333;
    padding: 10px 14px;
    border-radius: 12px;
    margin: 8px 0;
    text-align: left;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

/* Header */
.header {
    background-color: #0078ff;
    color: white;
    padding: 12px;
    border-radius: 10px;
    text-align: center;
    font-size: 20px;
    font-weight: bold;
    box-shadow: 0 2px 10px rgba(0,120,255,0.3);
    margin-bottom: 10px;
}

</style>

<!-- Floating bubbles -->
<div class="bubbles" id="bubbles"></div>

<script>
const bubbleContainer = document.getElementById("bubbles");

for (let i = 0; i < 35; i++) {
    let bubble = document.createElement("div");
    bubble.className = "bubble";

    let size = Math.random() * 20 + 10;

    bubble.style.left = Math.random() * 100 + "%";
    bubble.style.width = size + "px";
    bubble.style.height = size + "px";

    bubble.style.animationDuration = (Math.random() * 5 + 6) + "s";
    bubble.style.animationDelay = Math.random() * 5 + "s";

    bubbleContainer.appendChild(bubble);
}
</script>
""", unsafe_allow_html=True)


st.markdown('<div class="header">🛍️ AI Sales Assistant</div>', unsafe_allow_html=True)


api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("⚠️ GOOGLE_API_KEY not found in .env file.")
    st.stop()


if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "chatbot" not in st.session_state:
    st.session_state.chatbot = ChatbotLogic(api_key=api_key)

chatbot = st.session_state.chatbot

if "messages" not in st.session_state:
    st.session_state.messages = chatbot.get_chat_history_for_display(
        st.session_state.session_id
    )

st.markdown('<div class="chat-container">', unsafe_allow_html=True)


for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(
            f'<div class="user-msg">{message["content"]}</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="bot-msg">{message["content"]}</div>',
            unsafe_allow_html=True
        )

st.markdown('</div>', unsafe_allow_html=True)


prompt = st.chat_input("Type your message...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Thinking..."):
        bot_response = chatbot.process_query(
            prompt,
            st.session_state.session_id
        )

    st.session_state.messages.append(
        {"role": "assistant", "content": bot_response}
    )

    st.rerun()
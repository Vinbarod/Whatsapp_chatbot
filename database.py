import sqlite3

DATABASE_NAME = "chat_history.db"

def init_db():
    """Initializes the SQLite database and creates the chat_history table if it doesn't exist."""
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    print(f"Database '{DATABASE_NAME}' initialized successfully.")

def add_message(session_id, role, content):
    """Adds a chat message to the database."""
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO chat_history (session_id, role, content) VALUES (?, ?, ?)",
                       (session_id, role, content))
        conn.commit()

def get_chat_history(session_id, limit=10):
    """Retrieves the last 'limit' messages for a given session_id."""
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT role, content FROM chat_history WHERE session_id = ? ORDER BY timestamp DESC LIMIT ?",
                       (session_id, limit))
        
        history = cursor.fetchall()
        return [{'role': row[0], 'content': row[1]} for row in reversed(history)]

def clear_chat_history(session_id):
    """Clears the chat history for a specific session."""
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM chat_history WHERE session_id = ?", (session_id,))
        conn.commit()
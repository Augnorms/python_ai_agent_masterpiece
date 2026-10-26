import sqlite3
import json

DB_NAME = "agent_memory.db"

def init_db():
    """Creates the database and table if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # We store the entire messages array as a JSON string
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_sessions (
            session_id TEXT PRIMARY KEY,
            messages TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_history(session_id: str, messages: list):
    """Saves the chat history for a specific session."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create a clean list of messages with ONLY the fields the API accepts
    clean_messages = []
    for msg in messages:
        # Convert Pydantic object to dict if necessary
        if hasattr(msg, "model_dump"):
            msg_dict = msg.model_dump()
        else:
            msg_dict = dict(msg)
            
        clean_msg = {"role": msg_dict.get("role")}
        
        if msg_dict.get("content") is not None:
            clean_msg["content"] = msg_dict["content"]
            
        if msg_dict.get("tool_calls"):
            clean_msg["tool_calls"] = msg_dict["tool_calls"]
            
        if msg_dict.get("tool_call_id"):
            clean_msg["tool_call_id"] = msg_dict["tool_call_id"]
            
        clean_messages.append(clean_msg)

    # Convert the clean Python list to a JSON string
    messages_json = json.dumps(clean_messages)
    
    # Insert or replace if the session already exists
    cursor.execute("""
        INSERT OR REPLACE INTO chat_sessions (session_id, messages)
        VALUES (?, ?)
    """, (session_id, messages_json))
    
    conn.commit()
    conn.close()

def load_history(session_id: str) -> list:
    """Loads the chat history for a specific session."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT messages FROM chat_sessions WHERE session_id = ?", (session_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return json.loads(row[0])
    return [] # Return empty list if no history found

def get_all_users():
    """Reads all users from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Create a dummy table if it doesn't exist, and insert fake data
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com'), ('Bob', 'bob@example.com')")
        conn.commit()
        
    cursor.execute("SELECT id, name, email FROM users")
    users = cursor.fetchall()
    conn.close()
    
    if not users:
        return "No users found in the database."
        
    result = "Users in database:\n"
    for u in users:
        result += f"- ID: {u[0]}, Name: {u[1]}, Email: {u[2]}\n"
    return result


def delete_user(user_id: int):
    """Deletes a user by ID."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return f"User with ID {user_id} was successfully deleted."


def delete_session(session_id: str):
    """Deletes a specific chat session from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chat_sessions WHERE session_id = ?", (session_id,))
    conn.commit()
    conn.close()

# Initialize the database when this file is imported
init_db()
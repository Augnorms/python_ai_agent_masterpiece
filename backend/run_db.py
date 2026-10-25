import sqlite3

conn = sqlite3.connect("agent_memory.db")
cursor = conn.cursor()
cursor.execute("SELECT session_id, messages FROM chat_sessions")
rows = cursor.fetchall()

for row in rows:
    print(f"Session ID: {row[0]}")
    print(f"History: {row[1]}")
    print("-" * 50)

conn.close()
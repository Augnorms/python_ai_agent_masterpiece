import sqlite3
conn = sqlite3.connect("agent_memory.db")
cursor = conn.cursor()
cursor.execute("DELETE FROM chat_sessions") # Clears all chat history
conn.commit()
conn.close()
print("SQLite chat history cleared!")
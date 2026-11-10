from database.database import get_db_connection

def clear_all_chats():
    print("Connecting to database...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # This deletes EVERY row in the chat_sessions table
        cursor.execute("DELETE FROM chat_sessions")
        conn.commit()
        print("Successfully cleared all chat sessions from the database.")
    except Exception as e:
        print(f"Error clearing database: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    clear_all_chats()
import psycopg2
import psycopg2.extras
import json

DB_HOST = "localhost"
DB_NAME = "agent_memory"
DB_USER = "admin"
DB_PASS = "secretpassword"
DB_PORT = "5432"

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )

def init_db():
    """Creates the tables if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create chat_sessions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_sessions (
            session_id VARCHAR(255) PRIMARY KEY,
            messages TEXT
        )
    """)
    
    # 1. Create users table for Authentication
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS auth_users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            hashed_password VARCHAR(255) NOT NULL
        )
    """)

    # Create document_chunks table for Hybrid Search
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS document_chunks (
            id SERIAL PRIMARY KEY,
            filename VARCHAR(255),
            content TEXT
        )
    """)

    # Create swarm_settings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS swarm_settings (
            session_id VARCHAR(255) PRIMARY KEY DEFAULT 'default',
            is_swarm_active BOOLEAN DEFAULT TRUE,
            swarm_mode VARCHAR(100) DEFAULT 'autonomous',
            max_steps INT DEFAULT 10,
            supervisor_model VARCHAR(255) DEFAULT 'openai/gpt-oss-120b',
            custom_model_id VARCHAR(255) DEFAULT '',
            temperature FLOAT DEFAULT 0.2,
            embedding_model VARCHAR(255) DEFAULT 'all-MiniLM-L6-v2',
            active_agents JSONB DEFAULT '["rag_agent", "database_agent", "weather_agent", "email_agent"]'::jsonb,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        INSERT INTO swarm_settings (
            session_id,
            is_swarm_active,
            swarm_mode,
            max_steps,
            supervisor_model,
            custom_model_id,
            temperature,
            embedding_model,
            active_agents
        ) VALUES (
            'default',
            TRUE,
            'autonomous',
            10,
            'openai/gpt-oss-120b',
            '',
            0.2,
            'all-MiniLM-L6-v2',
            '["rag_agent", "database_agent", "weather_agent", "email_agent"]'::jsonb
        ) ON CONFLICT (session_id) DO NOTHING;
    """)

    conn.commit()
    cursor.close()
    conn.close()


"""
###############################################
     database queries goes down here....
###############################################

"""

def create_auth_user(username: str, email: str, hashed_password: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO auth_users (username, email, hashed_password) VALUES (%s, %s, %s) RETURNING id",
            (username, email, hashed_password)
        )
        user_id = cursor.fetchone()[0]
        conn.commit()
        return user_id
    except psycopg2.IntegrityError:
        conn.rollback()
        return None # Username or email already exists
    finally:
        cursor.close()
        conn.close()

def get_auth_user_by_username(username: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, hashed_password FROM auth_users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if user:
        return {"id": user[0], "username": user[1], "email": user[2], "hashed_password": user[3]}
    return None

def get_all_users():
    """Retrieves all users from the auth_users table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email FROM auth_users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"id": u[0], "username": u[1], "email": u[2]} for u in users]

def delete_user(user_id: int):
    """Deletes a user from the auth_users table by user_id."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM auth_users WHERE id = %s", (user_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    cursor.close()
    conn.close()
    if deleted:
        return f"User with ID {user_id} successfully deleted."
    return f"User with ID {user_id} not found."


def save_history(session_id: str, messages: list):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    clean_messages = []
    for msg in messages:
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

    messages_json = json.dumps(clean_messages)
    
    # Postgres INSERT OR REPLACE is done via ON CONFLICT
    cursor.execute("""
        INSERT INTO chat_sessions (session_id, messages)
        VALUES (%s, %s)
        ON CONFLICT (session_id) DO UPDATE SET messages = EXCLUDED.messages;
    """, (session_id, messages_json))
    
    conn.commit()
    cursor.close()
    conn.close()


def load_history(session_id: str) -> list:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT messages FROM chat_sessions WHERE session_id = %s", (session_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if row:
        return json.loads(row[0])
    return []


def delete_session(session_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chat_sessions WHERE session_id = %s", (session_id,))
    conn.commit()
    cursor.close()
    conn.close()


def save_document_chunks(filename: str, chunks: list):
    """Saves text chunks to Postgres for keyword search."""
    conn = get_db_connection()
    cursor = conn.cursor()
    # Clear old chunks for this file to avoid duplicates
    cursor.execute("DELETE FROM document_chunks WHERE filename = %s", (filename,))
    
    for chunk in chunks:
        cursor.execute(
            "INSERT INTO document_chunks (filename, content) VALUES (%s, %s)",
            (filename, chunk)
        )
    conn.commit()
    cursor.close()
    conn.close()


def keyword_search_chunks(query: str, limit=2):
    """Performs a keyword search in Postgres."""
    conn = get_db_connection()
    cursor = conn.cursor()
    # Using ILIKE for simple case-insensitive keyword matching
    cursor.execute("""
        SELECT content FROM document_chunks 
        WHERE content ILIKE %s 
        LIMIT %s
    """, (f"%{query}%", limit))
    
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return [row[0] for row in rows]


def clear_document_chunks():
    """Deletes all rows from the document_chunks table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM document_chunks")
    conn.commit()
    cursor.close()
    conn.close()


def get_swarm_settings(session_id: str = "default") -> dict:
    """Retrieves the swarm settings for a given session_id from the database.
    If session_id is 'default' or not found, automatically falls back to the most 
    recently saved user configuration in swarm_settings."""
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    row = None
    if session_id and session_id != "default":
        cursor.execute("SELECT * FROM swarm_settings WHERE session_id = %s", (session_id,))
        row = cursor.fetchone()

    # If no row exists for this session or if requesting 'default', fall back to the most recently updated settings
    if not row:
        cursor.execute("SELECT * FROM swarm_settings ORDER BY updated_at DESC NULLS LAST LIMIT 1")
        row = cursor.fetchone()

    # If table is completely empty, supply robust default configuration
    if not row:
        row = {
            "session_id": session_id or "default",
            "is_swarm_active": True,
            "swarm_mode": "autonomous",
            "max_steps": 10,
            "supervisor_model": "openai/gpt-oss-20b",
            "custom_model_id": "",
            "temperature": 0.2,
            "embedding_model": "all-MiniLM-L6-v2",
            "active_agents": ["rag_agent", "database_agent", "weather_agent", "email_agent"],
            "updated_at": None
        }

    cursor.close()
    conn.close()

    if row:
        row_dict = dict(row)
        if "updated_at" in row_dict and row_dict["updated_at"]:
            row_dict["updated_at"] = row_dict["updated_at"].isoformat()
        return row_dict
    return {}


def update_swarm_settings(
    session_id: str = "default",
    is_swarm_active: bool = None,
    swarm_mode: str = None,
    max_steps: int = None,
    supervisor_model: str = None,
    custom_model_id: str = None,
    temperature: float = None,
    embedding_model: str = None,
    active_agents=None
) -> dict:
    """Updates the swarm configuration row for a given session_id in PostgreSQL."""
    if not session_id:
        session_id = "default"
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Ensure the row exists for this session_id first
    cursor.execute("""
        INSERT INTO swarm_settings (session_id, is_swarm_active, swarm_mode, max_steps, supervisor_model, custom_model_id, temperature, embedding_model, active_agents)
        VALUES (%s, TRUE, 'autonomous', 10, 'openai/gpt-oss-120b', '', 0.2, 'all-MiniLM-L6-v2', '["rag_agent", "database_agent", "weather_agent", "email_agent"]'::jsonb)
        ON CONFLICT (session_id) DO NOTHING
    """, (session_id,))
    conn.commit()

    update_fields = []
    params = []

    if is_swarm_active is not None:
        update_fields.append("is_swarm_active = %s")
        params.append(is_swarm_active)
    if swarm_mode is not None:
        update_fields.append("swarm_mode = %s")
        params.append(swarm_mode)
    if max_steps is not None:
        update_fields.append("max_steps = %s")
        params.append(max_steps)
    if supervisor_model is not None:
        update_fields.append("supervisor_model = %s")
        params.append(supervisor_model)
    if custom_model_id is not None:
        update_fields.append("custom_model_id = %s")
        params.append(custom_model_id)
    if temperature is not None:
        update_fields.append("temperature = %s")
        params.append(temperature)
    if embedding_model is not None:
        update_fields.append("embedding_model = %s")
        params.append(embedding_model)
    if active_agents is not None:
        update_fields.append("active_agents = %s")
        if isinstance(active_agents, (list, dict)):
            params.append(json.dumps(active_agents))
        else:
            params.append(str(active_agents))

    if update_fields:
        update_fields.append("updated_at = CURRENT_TIMESTAMP")
        params.append(session_id)
        query = f"UPDATE swarm_settings SET {', '.join(update_fields)} WHERE session_id = %s RETURNING *"
        cursor.execute(query, tuple(params))
        row = cursor.fetchone()
        if session_id != "default":
            # Also keep the 'default' session row synchronized with latest global settings
            default_params = list(params[:-1]) + ["default"]
            cursor.execute(query, tuple(default_params))
        conn.commit()
    else:
        cursor.execute("SELECT * FROM swarm_settings WHERE session_id = %s", (session_id,))
        row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row:
        row_dict = dict(row)
        if "updated_at" in row_dict and row_dict["updated_at"]:
            row_dict["updated_at"] = row_dict["updated_at"].isoformat()
        return row_dict
    return {}

# Initialize tables on import
init_db()

from fastapi import APIRouter
from database.database import load_history

router = APIRouter()


@router.get("/api/history")
async def get_history(session_id: str):
    history = load_history(session_id)

    # We only want to send the user and assistant text to the frontend,
    # ignoring the messy tool calls and system prompts.
    chat_messages = []
    for msg in history:
        # Check if it's a dict or an object from Pydantic
        role = msg.get("role") if isinstance(msg, dict) else getattr(msg, "role", "")
        content = msg.get("content") if isinstance(msg, dict) else getattr(msg, "content", "")

        # We only want to show user messages and final assistant answers
        if role == "user" and not content.startswith("Before you finalize"):
            chat_messages.append({"role": "user", "text": content})
        elif role == "assistant" and content and "Final Answer:" in content:
            chat_messages.append({"role": "agent", "text": content})

    return {"messages": chat_messages}

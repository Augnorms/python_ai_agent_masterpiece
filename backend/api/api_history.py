from fastapi import APIRouter
from database.database import load_history
import re

router = APIRouter()


def extract_final_answer(content: str) -> str:
    """Extracts only the final answer text, stripping out thoughts and prefixes."""
    if not content:
        return ""
    text = content.strip()

    # 1. Strip explicit Final Answer markers
    if "[Final Answer]" in text:
        text = text.split("[Final Answer]")[-1].strip()
    elif "Final Answer:" in text:
        text = text.split("Final Answer:")[-1].strip()
    elif "final answer:" in text.lower():
        idx = text.lower().rfind("final answer:")
        text = text[idx + len("final answer:"):].strip()
    else:
        # 2. If message begins with a Thought block, strip the thoughts
        if re.match(r'^\*?\*?Thought:\*?\*?', text, re.IGNORECASE):
            parts = re.split(r'\n\s*\n', text, maxsplit=1)
            if len(parts) > 1:
                text = parts[1].strip()

    return text


@router.get("/api/history")
async def get_history(session_id: str):
    history = load_history(session_id)

    chat_messages = []
    for msg in history:
        role = msg.get("role") if isinstance(msg, dict) else getattr(msg, "role", "")
        content = msg.get("content") if isinstance(msg, dict) else getattr(msg, "content", "")
        tool_calls = msg.get("tool_calls") if isinstance(msg, dict) else getattr(msg, "tool_calls", None)

        # 1. User messages (skip internal guardrail / reflection injected prompts)
        if role == "user":
            if content and not content.startswith("Before you finalize") and not content.startswith("You did arithmetic"):
                chat_messages.append({"role": "user", "text": content})

        # 2. Assistant messages with text (extract only the clean final answer)
        elif role == "assistant" and content and not tool_calls:
            answer = extract_final_answer(content)
            if answer:
                # If an answer was already recorded for this turn (e.g. before reflection review),
                # replace it with the latest finalized response.
                if chat_messages and chat_messages[-1]["role"] == "agent":
                    chat_messages[-1]["text"] = answer
                else:
                    chat_messages.append({"role": "agent", "text": answer})

    return {"messages": chat_messages}


from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import asyncio
import queue
import json
import threading
import time

from agent_folder.manager import MANAGER_TOOLS_SCHEMA, get_manager_tools
from agent_folder.agent import run_agent
from database.database import load_history, save_history
from api.state import approval_events, approval_results

router = APIRouter()


@router.get("/api/chat")
async def chat_endpoint(prompt: str, session_id: str):
    # Create a thread-safe queue to hold our messages
    message_queue = queue.Queue()

    # Task emitter for the left-side execution panel
    def agent_task_emitter(task_event):
        message_queue.put({"type": "task_event", "data": task_event})

    # Logger function passed to the agent
    def agent_logger(message):
        message_queue.put({"type": "text", "data": str(message)})

    # HITL Callback
    def approval_callback(tool_name, tool_args):
        message_queue.put({
            "type": "text",
            "data": f"[WAITING_FOR_APPROVAL] Tool: {tool_name}, Args: {json.dumps(tool_args)}"
        })

        event = threading.Event()
        approval_events[session_id] = event
        event.wait(timeout=60)
        result = approval_results.get(session_id, False)

        del approval_events[session_id]
        if session_id in approval_results:
            del approval_results[session_id]

        return result

    # Background worker running the synchronous agent
    def run_agent_task():
        start_time = time.time()
        success = True

        try:
            message_queue.put({"type": "text", "data": "[System] Agent thinking..."})

            history = load_history(session_id)

            answer, updated_history = run_agent(
                prompt,
                history,
                MANAGER_TOOLS_SCHEMA,
                get_manager_tools(agent_logger, approval_callback=approval_callback, task_emitter=agent_task_emitter, session_id=session_id),
                use_guardrails=True,
                logger=agent_logger,
                approval_callback=approval_callback,
                task_emitter=agent_task_emitter,
                session_id=session_id
            )

            save_history(session_id, updated_history)

            elapsed_ms = int((time.time() - start_time) * 1000)

            message_queue.put({"type": "text", "data": f"[Final Answer] {answer}"})
            message_queue.put({
                "type": "metrics",
                "data": {"latency_ms": elapsed_ms, "success": success}
            })

        except Exception as e:
            message_queue.put({"type": "text", "data": f"[Error] {e}"})
        finally:
            message_queue.put(None)

    asyncio.create_task(asyncio.to_thread(run_agent_task))

    async def event_stream():
        while True:
            msg = await asyncio.to_thread(message_queue.get)
            if msg is None:
                break
            yield f"data: {json.dumps(msg)}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

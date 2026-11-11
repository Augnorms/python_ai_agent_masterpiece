from fastapi import APIRouter, Query, Depends
from fastapi.responses import StreamingResponse
import asyncio
import queue
import json

from auto_agent_service import trigger_agent_run, get_last_agent_run
from api.auth import get_current_user

router = APIRouter()

@router.api_route("/api/agent/auto-run", methods=["GET", "POST"])
async def run_plant_agent(run_now: bool = Query(True), current_user: dict = Depends(get_current_user)):
    user_email = current_user.get("email")
    if not user_email:
        username = current_user.get("username", "admin")
        user_email = f"{username}@aquasync-desal.internal"

    if not run_now:
        last = get_last_agent_run()
        if last.get("diagnostic_report"):
            return last

    # Create thread-safe queue for SSE message passing
    message_queue = queue.Queue()

    # Background worker running synchronous agent execution
    asyncio.create_task(asyncio.to_thread(trigger_agent_run, user_email, message_queue))

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

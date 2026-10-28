from fastapi import APIRouter, Request
from api.state import approval_events, approval_results

router = APIRouter()


@router.post("/api/approve")
async def approve_action(request: Request):
    data = await request.json()
    session_id = data.get("session_id")
    is_approved = data.get("approved", False)

    if session_id in approval_events:
        # 1. Save the user's decision
        approval_results[session_id] = is_approved
        # 2. Unblock the background thread!
        approval_events[session_id].set()
        return {"status": "success"}

    return {"status": "error", "message": "No pending approval for this session"}

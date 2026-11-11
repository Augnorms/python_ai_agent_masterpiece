from fastapi import APIRouter, Query
from auto_agent_service import trigger_agent_run, get_last_agent_run
from api.auth import get_current_user
from fastapi import Depends

router = APIRouter()

@router.api_route("/api/agent/auto-run", methods=["GET", "POST"])
def run_palnt_agent(run_now: bool = Query(True), current_user: dict = Depends(get_current_user)):
    user_email = current_user.get("email")
    if not user_email:
        username = current_user.get("username", "admin")
        user_email = f"{username}@aquasync-desal.internal"

    if not run_now:
        last = get_last_agent_run()
        if last.get("diagnostic_report"):
            return last
    result = trigger_agent_run(recipient_email=user_email)
    return result

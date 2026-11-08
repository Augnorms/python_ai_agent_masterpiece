from fastapi import APIRouter, Query
from auto_agent_service import trigger_agent_run, get_last_agent_run

router = APIRouter()

@router.api_route("/api/agent/auto-run", methods=["GET", "POST"])
def run_palnt_agent(run_now: bool = Query(True)):
    if not run_now:
        last = get_last_agent_run()
        if last.get("diagnostic_report"):
            return last
    result = trigger_agent_run()
    return result

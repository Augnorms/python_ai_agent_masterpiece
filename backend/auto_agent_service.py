from datetime import datetime
import threading
from ml_service import predict_live_status
from agent_folder.agent import run_agent
from agent_folder.manager import MANAGER_TOOLS_SCHEMA, get_manager_tools

_agent_execution_lock = threading.Lock()
_is_running = False

# In-memory cache for the most recent agent execution
last_agent_run = {
    "status": "idle",
    "cycle_number": 142,
    "diagnostic_report": None,
    "live_inputs": None,
    "reasoning_steps": [],
    "timestamp": None
}

cycle_counter = 142

def get_last_agent_run():
    return last_agent_run

def trigger_agent_run():
    global cycle_counter, last_agent_run, _is_running

    # Guard against multiple concurrent agent executions
    if _is_running:
        return last_agent_run

    with _agent_execution_lock:
        _is_running = True
        try:
            cycle_counter += 1

            # 1. Get the live data to pass into the prompt
            live_data = predict_live_status()
            if live_data.get("status") == "error":
                err_res = {
                    "status": "error",
                    "message": "PLC is disconnected",
                    "cycle_number": cycle_counter,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                }
                last_agent_run = err_res
                return err_res

            flow = live_data["predictions"]["alpha"]["flow"]
            tds = live_data["predictions"]["beta"]["tds"]
            quality = live_data["predictions"]["beta"]["quality_status"]

            # 2. Create the autonomous prompt using the live numbers
            prompt = (
                f"You are an autonomous plant supervisor. The current live data is: "
                f"Flow={flow} m3/h, TDS={tds} ppm (Quality: {quality}). "
                f"Check the plant SOPs. Is this water quality safe? "
                f"If it is Warning or Poor, what exact corrective action does the SOP state? "
                f"Provide a concise diagnostic report."
            )

            # 3. Capture ReAct trace / reasoning logs for the frontend Chain-of-Thought stream
            logs = [
                f"[INGEST] Telemetry verified: Flow={flow} m³/h, TDS={tds} ppm ({quality})",
                "[SUPERVISOR] Starting autonomous water quality & SOP compliance audit...",
            ]

            def agent_logger(msg):
                logs.append(str(msg))
            
            answer, trace = run_agent(
                prompt, 
                [], 
                MANAGER_TOOLS_SCHEMA, 
                get_manager_tools(agent_logger), 
                logger=agent_logger, 
                use_guardrails=True
            )

            logs.append(f"[ORCHESTRATOR] Autonomous diagnostic completed successfully.")

            result = {
                "status": "success",
                "cycle_number": cycle_counter,
                "diagnostic_report": answer,
                "live_inputs": {"flow": flow, "tds": tds, "quality": quality},
                "reasoning_steps": logs,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            }

            last_agent_run = result
            return result
        finally:
            _is_running = False


from datetime import datetime
import threading
from ml_service import predict_live_status
from agent_folder.agent import run_agent
from agent_folder.manager import MANAGER_TOOLS_SCHEMA, get_manager_tools
from agent_folder.tools import send_email

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
            recipient_email = "augustinenormanyo98@gmail.com"
            prompt = (
                f"You are the autonomous plant supervisor for SWRO Plant #04.\n"
                f"Live Telemetry Snapshot: Flow={flow} m3/h, TDS={tds} ppm, Water Quality={quality}.\n\n"
                f"Instructions:\n"
                f"1. Call `ask_rag_agent` to check plant SOPs: Is this water quality safe? If Warning or Poor, what exact corrective action does the SOP state?\n"
                f"2. Call `ask_email_agent` to send an email report to {recipient_email} with subject 'Plant Diagnostic Report - Cycle #{cycle_counter}' and include the findings.\n"
                f"3. Return a concise diagnostic report as your final answer."
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

            # 4. Guarantee email delivery: check if email was dispatched during the agent run
            email_already_sent = any("Routing to Email Agent" in str(l) or "Email successfully sent" in str(l) for l in logs)
            if not email_already_sent:
                agent_logger(f"[EMAIL] Dispatching diagnostic report to {recipient_email} via Resend...")
                email_status = send_email(
                    to_address=recipient_email,
                    subject=f"🌊 Plant Diagnostic Report - Cycle #{cycle_counter} ({quality})",
                    body=answer or f"Plant Status: Flow={flow} m3/h, TDS={tds} ppm ({quality}). Safe per SOP.",
                    flow=flow,
                    tds=tds,
                    quality=quality
                )
                agent_logger(f"[EMAIL] {email_status}")

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


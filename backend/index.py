from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import asyncio
import queue
import json
from agent_folder.manager import MANAGER_TOOLS_SCHEMA, get_manager_tools 
from agent_folder.agent import run_agent
from database.database import load_history, save_history, delete_session
import threading
import time

app = FastAPI()

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# A global dictionary to hold the Event objects for each session
# { "session_id": threading.Event() }
approval_events = {}
approval_results = {} # { "session_id": True/False }


@app.get("/api/chat")
async def chat_endpoint(prompt: str, session_id: str):
    # Create a thread-safe queue to hold our messages
    message_queue = queue.Queue()

        # Task emitter for the left-side execution panel
    def agent_task_emitter(task_event):
        # Send a special JSON payload to the frontend
        message_queue.put({"type": "task_event", "data": task_event})

    # Logger function passed to the agent
    def agent_logger(message):
        message_queue.put({"type": "text", "data": str(message)})

    # --- NEW: HITL Callback ---
    def approval_callback(tool_name, tool_args):
        # 1. Tell the frontend we need approval
        message_queue.put({"type": "text", "data": f"[WAITING_FOR_APPROVAL] Tool: {tool_name}, Args: {json.dumps(tool_args)}"})
        
        # 2. Create an Event and store it
        event = threading.Event()
        approval_events[session_id] = event
        
        # 3. Block this background thread until the event is set (by the frontend)
        event.wait(timeout=60) 
        
        # 4. Return the result (True or False) that the frontend set
        result = approval_results.get(session_id, False)
        
        # Cleanup
        del approval_events[session_id]
        if session_id in approval_results:
            del approval_results[session_id]
            
        return result
    # ----------------------------

    # Background worker running the synchronous agent
    def run_agent_task():
        start_time = time.time()
        success = True

        try:
            message_queue.put({"type": "text", "data": "[System] Agent thinking..."})

            # 1. LOAD HISTORY FROM DATABASE
            history = load_history(session_id)

            answer, updated_history = run_agent(
                prompt,
                history,
                MANAGER_TOOLS_SCHEMA,
                get_manager_tools(agent_logger, approval_callback=approval_callback, task_emitter=agent_task_emitter),
                use_guardrails=True,
                logger=agent_logger,
                approval_callback=approval_callback, 
                task_emitter=agent_task_emitter
            )

            # 3. SAVE UPDATED HISTORY TO DATABASE
            save_history(session_id, updated_history)

            # Calculate metrics
            elapsed_ms = int((time.time() - start_time) * 1000)

            message_queue.put({"type": "text", "data": f"[Final Answer] {answer}"})

            # Send the metric event to the frontend
            message_queue.put({
                "type": "metrics", 
                "data": {"latency_ms": elapsed_ms, "success": success}
            })
            
        except Exception as e:
            message_queue.put({"type": "text", "data": f"[Error] {e}"})
        finally:
            message_queue.put(None)  # Sentinel to end the stream
            success = False

    # Start the agent thread in the background
    asyncio.create_task(asyncio.to_thread(run_agent_task))

    # Stream generator yielding events to the browser
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

@app.get("/api/history")
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



@app.post("/api/approve")
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



@app.delete("/api/memory/{session_id}")
async def clear_memory(session_id: str):
    delete_session(session_id)
    return {"status": "success", "message": "Memory cleared"}


@app.get("/api/status")
async def get_status():
    # In a real app, you might query the cloud provider here. 
    # For now, we hardcode it to match your screenshot.
    return {
        "status": "active",
        "region": "Ghana-Accra",
        "model": "openai/gpt-oss-20b"
    }
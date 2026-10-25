from openai.resources.beta.threads import messages
from agent_folder.client import client
from agent_folder.guardrails import is_prompt_injection, detect_math, did_use_math_previously
import json

system_input = """
You are an AI assistant. 
Before you call a tool, you must write out your reasoning in the 'content' field using the format:
Thought: [Your reasoning]

Then, use the provided tools to take the action. 
Once you have the final answer, write:
Thought: I now know the final answer.
Final Answer: [Your answer]
"""

DANGEROUS_TOOLS = ["delete_user", "send_email"]

def run_agent(
     user_input,
     messages, 
     available_tools, 
     tool_functions, 
     system_input=system_input, 
     maxstep=80, 
     use_guardrails=True, 
     logger=print,
     approval_callback=None
     ):

    if not messages:
        messages = [{"role": "system", "content": system_input}] 
 
    #checks input guardrails
    if is_prompt_injection(user_input):
        logger("[security guardrail] Blocked prompt injection attempt.")
        return "I cannot fulfill this request due to security policies.", []

    #Append the new message to the history (do NOT overwrite it)
    messages.append({"role": "user", "content": user_input})

    reflection_done = False

    for i in range(maxstep):
        try:
            response = client.chat.completions.create(
                model="qwen/qwen3.8-27b",
                messages=messages,
                tools=available_tools
            )
        except Exception as e:
            logger(f"[API Error] {e}")
            return f"API Error occurred: {e}", messages

        assistant_message = response.choices[0].message
        tool_calls = assistant_message.tool_calls
        
        #print(tool_calls)
        messages.append(assistant_message)

        #this is the final answer
        #if tool_call is empty then call the content
        if not tool_calls:
            if use_guardrails:
                # 2. GUARDRAIL: Did they ask for math, but NEVER use a math tool in the whole trace?
                if detect_math(user_input) and not did_use_math_previously(messages):
                    logger(f"[guardrail] violation — LLM tried to finish without using a math tool")

                    messages.append({
                        "role":"user",
                        "content":"You did arithmetic without calling a tool. You must call add, multiply, or substraction. Retry."
                    })
                    continue # Reject the answer, force a retry

                        # --- NEW: REFLECTION ---
            if not reflection_done:
                logger("[reflection] Asking LLM to review its answer...")
                messages.append({
                    "role": "user",
                    "content": "Before you finalize, review your answer. If there is an error, fix it. If it is correct, output your final answer again exactly as it was, but do NOT include the review process in your final output."
                })
                reflection_done = True
                continue # Loop back so the LLM can review

            #No violation, return the final answer
            return assistant_message.content, messages
            

        for tool_call in tool_calls:
            tool_call_id  = tool_call.id
            tool_args = json.loads(tool_call.function.arguments)
            tool_name = tool_call.function.name

            # --- HUMAN IN THE LOOP GUARDRAIL ---
            if tool_name in DANGEROUS_TOOLS:
                if approval_callback:
                    logger(f"[HITL] Pausing execution. Waiting for human approval for {tool_name}({tool_args})...")
                    # This will block the thread until the user clicks Approve/Deny in the UI
                    is_approved = approval_callback(tool_name, tool_args) 
                    
                    if not is_approved:
                        logger("[HITL] Execution Denied by human.")
                        messages.append({
                            "role":"tool",
                            "tool_call_id":tool_call_id,
                            "content":"Error: The human operator denied the execution of this tool. You must stop and inform the user."
                        })
                        continue
                else:
                    logger("[HITL] WARNING: Dangerous tool called but no approval callback provided. Skipping.")
                    messages.append({
                        "role":"tool",
                        "tool_call_id":tool_call_id,
                        "content":"Error: Dangerous tool execution blocked (no approval mechanism)."
                    })
                    continue
            # -----------------------------------

            try:
                logger(f"[step {i}] calling {tool_name}({tool_args})")

                result = tool_functions[tool_name](**tool_args)
                
                logger(f"[step {i}] -> {result}")
            except Exception as e:
                result = f"Error {e}"
            
            messages.append({
                "role":"tool",
                "tool_call_id":tool_call_id,
                "content":str(result)
            })

    return "Hit max steps without a final answer.", messages




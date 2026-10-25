from agent_folder.client import client


MATH_TOOLS = {"add", "multiply", "substraction"}
MATH_WORDS = ["plus", "minus", "times", "multiply", "add", "subtract",
              "divide", "sum", "total", "+", "-", "*", "/"]
PROMPT_INPUTS = ["ignore previous", "system prompt", "you are now", "override"]



def detect_math(user_input):
    """Guardrail to enforce usage of math functions"""
    words = user_input.lower().replace("?", "").replace(",", "").split()
    return any(word in MATH_WORDS for word in words)

def did_use_math_previously(messages):
    for msg in messages:
       
        if getattr(msg, "tool_calls", None):
            if any(call.function.name in MATH_TOOLS for call in msg.tool_calls):
                return True
    return False

def is_prompt_injection(user_input):
    text  = user_input.lower()
    if any(phrase in text for phrase in PROMPT_INPUTS):
        return True
    return False

def judge_tool_call(user_input, tool_name, tool_args):
    """ function call to judge the tool call """
    
    # 1. Inject the variables into the string using an f-string
    judge_prompt = f"""You are a strict tool auditor. Your job is to verify if a tool call matches the user's intent.

        The user asked: "{user_input}"
        The agent wants to call the tool: "{tool_name}"
        With the arguments: {tool_args}

        RULES:
        1. If the user asks to add, sum, or plus, the tool MUST be 'add'.
        2. If the user asks to multiply, times, or product, the tool MUST be 'multiply'.
        3. If the user asks to subtract or minus, the tool MUST be 'substraction'.
        4. If the user asks for weather, the tool MUST be 'getWeather'.

        Does the tool call follow these rules for the user's request?
        Reply with ONLY the word YES or NO. Do not explain."""

    # 2. Make the API call (must be a list of message dicts)
    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=[{"role": "user", "content": judge_prompt}],
        temperature=0.0 
    ) 
    
    # 3. Extract the text and check if it's YES
    answer = response.choices[0].message.content.strip().upper()
    return "YES" in answer


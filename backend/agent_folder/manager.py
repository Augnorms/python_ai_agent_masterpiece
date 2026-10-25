from inspect import trace
from agent_folder.agent import run_agent
from agent_folder.tools import MATH_TOOLS_SCHEMA, WEATHER_TOOLS_SCHEMA, TOOL_FUNCTION, DATABASE_TOOL_SCHEMA, EMAIL_TOOL_SCHEMA

def math_agent(question, logger, approval_callback=None):
    """A sub-agent that only knows how to do math."""
    logger("[Manager] Routing to Math Agent...")
    answer, trace = run_agent(question, [], MATH_TOOLS_SCHEMA, TOOL_FUNCTION, logger=logger, approval_callback=approval_callback)
    return answer        

def weather_agent(question, logger, approval_callback=None):
    """A sub-agent that only knows how to check the weather."""
    logger("[Manager] Routing to Weather Agent...")
    answer, trace = run_agent(question, [], WEATHER_TOOLS_SCHEMA, TOOL_FUNCTION, logger=logger, approval_callback=approval_callback)
    return answer

def database_query_agent(question, logger, approval_callback=None):
    """ Asub agent that performs database query """
    logger("[Manager] Routing to the database agent")
    answer, trace = run_agent(question, [], DATABASE_TOOL_SCHEMA, TOOL_FUNCTION, logger=logger, approval_callback=approval_callback)
    return answer

# 2. Add the email_agent function right below database_query_agent
def email_agent(question, logger, approval_callback=None):
    logger("[Manager] Routing to Email Agent...")
    answer, trace = run_agent(question, [], EMAIL_TOOL_SCHEMA, TOOL_FUNCTION, logger=logger, approval_callback=approval_callback)
    return answer


# 2. Define the Manager's Tools (What the Manager is allowed to call)
MANAGER_TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "ask_math_agent",
            "description": "Ask the math agent to solve any arithmetic, math, or calculation problem.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "The math question to ask"}
                },
                "required": ["question"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "ask_weather_agent",
            "description": "Ask the weather agent for the weather in a specific city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "The city name to check the weather for"}
                },
                "required": ["city"]
            }
        }
    },
        {
        "type": "function",
        "function": {
            "name": "ask_database_agent",
            "description": "Ask the database agent to perform database queries on the database",
            "parameters": {
                "type": "object",
                "properties":{
                    "question": {"type": "string", "description": "The database question to ask"}
                },
                "required": ["question"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "ask_email_agent",
            "description": "Ask the email agent to send an email to someone.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "The instructions for the email (who to send it to, subject, and body)"}
                },
                "required": ["question"]
            }
        }
    }
]

# 3. Define the Functions that the Manager actually executes
def ask_math_agent(question, logger=print):
    return math_agent(question, logger=print)

def ask_weather_agent(city):
    return weather_agent(f"What is the weather in {city}?")

def ask_database_agent(question, logger=print):
    return database_query_agent(question, logger=print)



"""
#####################################################################
                   manager too caller
#####################################################################
"""
def get_manager_tools(logger, approval_callback=None):
    def ask_math_agent(question):
        return math_agent(question, logger=logger, approval_callback=approval_callback)

    def ask_weather_agent(city):
        return weather_agent(f"What is the weather in {city}?", logger=logger, approval_callback=approval_callback)

    def ask_database_agent(question):
        return database_query_agent(question, logger=logger, approval_callback=approval_callback)

    def ask_email_agent(question):
        return email_agent(question, logger=logger, approval_callback=approval_callback)

    return {
        "ask_math_agent": ask_math_agent,
        "ask_weather_agent": ask_weather_agent,
        "ask_database_agent": ask_database_agent,
        "ask_email_agent": ask_email_agent
    }

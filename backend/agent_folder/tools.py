import requests
import os
import datetime
from database.database import get_all_users, delete_user


MATH_TOOLS_SCHEMA  = [
    {
        "type":"function",
        "function":{
            "name":"add",
            "description":"A function to add two numbers",
            "parameters":{
                "type":"object",
                "properties":{
                   "a":{"type":"number"},
                   "b":{"type":"number"}
                },
                "required":["a", "b"]
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"multiply",
            "description":"A function to multiply two numbers",
            "parameters":{
                "type":"object",
                "properties":{
                   "a":{"type":"number"},
                   "b":{"type":"number"}
                },
                "required":["a", "b"]
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"substraction",
            "description":"A function to substract two numbers",
            "parameters":{
                "type":"object",
                "properties":{
                    "a":{"type":"number"},
                    "b":{"type":"number"}
                },
                "required":["a", "b"]
            }
        }
    },

]

WEATHER_TOOLS_SCHEMA = [
        {
        "type":"function",
        "function":{
            "name":"get_weather",
            "description":"A function to get weather of a city",
            "parameters":{
                "type":"object",
                "properties":{
                    "city": {"type": "string"}
                },
                "required":["city"]
            }
        }
    }

]

DATABASE_TOOL_SCHEMA = [
    {
        "type":"function",
        "function":{
            "name":"get_all_users",
            "description":"A function to get_all_users from database",
            "parameters":{
                "type":"object",
                "properties":{},
                "required":[]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_user",
            "description": "Deletes a user from the database by their ID. Be very careful with this tool.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "The ID of the user to delete"}
                },
                "required": ["user_id"]
            }
        }
    }
]

EMAIL_TOOL_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "Sends an email to a specific address. Use this when the user asks to send an email.",
            "parameters": {
                "type": "object",
                "properties": {
                    "to_address": {"type": "string", "description": "The email address to send to"},
                    "subject": {"type": "string", "description": "The subject of the email"},
                    "body": {"type": "string", "description": "The content of the email"}
                },
                "required": ["to_address", "subject", "body"]
            }
        }
    }
]

def add(a, b):
    """ function to add two numbers  """
    return a + b

def multiply(a, b):
    """ function to multiple numbers """
    return a * b

def substraction(a, b):
    """function to substract numbers"""
    return a - b

# def get_weather(city):
#     """ function to get the weather of a city """
#     weather = {
#         "Wilmington": "Sunny, 10°C",
#         "Los Angeles": "Rainy, 30°C",
#         "New York": "Cloudy, 15°C",
#         "London": "Rainy, 12°C",
#         "Paris": "Windy, 14°C",
#         "Tokyo": "Sunny, 22°C",
#         "Sydney": "Sunny, 25°C",
#         "Dubai": "Sunny, 38°C",
#         "Accra": "Cloudy, 29°C",
#         "Cairo": "Sunny, 33°C",
#     }

def send_email(to_address: str, subject: str, body: str):
    """A mock function to send an email and write it to a log file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] To: {to_address} | Subject: {subject} | Body: {body}\n"
    
    # Write to a file in the backend folder
    with open("sent_emails.log", "a", encoding="utf-8") as f:
        f.write(log_entry)
        
    return f"Email successfully sent to {to_address}."

def get_weather(city):
    """ function to get the weather of a city using a real API """
    try:
        # Step 1: Geocode the city name to get lat/lon
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        geo_res = requests.get(geo_url).json()
        
        if "results" not in geo_res:
            raise ValueError(f"City '{city}' not found.")
            
        lat = geo_res["results"][0]["latitude"]
        lon = geo_res["results"][0]["longitude"]
        official_name = geo_res["results"][0]["name"]

        # Step 2: Fetch the weather using lat/lon
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_res = requests.get(weather_url).json()
        
        current = weather_res["current_weather"]
        temp = current["temperature"]
        wind = current["windspeed"]
        
        return f"{official_name}: {temp}°C, wind speed {wind} km/h"

    except Exception as e:
        raise ValueError(f"Failed to get weather: {str(e)}")

    city_name = city.title()
    if city_name not in weather:
        # Trigger the ValueError here:
        raise ValueError(f"City '{city}' not found in database. Supported cities: {list(weather.keys())}")

    return f"{city}: " + weather.get(city.title(), "No data available")


TOOL_FUNCTION = {
    "add":add,
    "multiply":multiply,
    "substraction":substraction,
    "get_weather": get_weather,
    "get_all_users": get_all_users,
    "delete_user": delete_user,
    "send_email": send_email 
}
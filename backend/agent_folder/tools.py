import requests
import os
import datetime
from database.database import get_all_users, delete_user, keyword_search_chunks
import chromadb
from sentence_transformers import SentenceTransformer
from inject_rag.ingest_rag_service import get_embedding_model
from ml_service import predict_live_status

#connect to chroma database using client
chroma_client = chromadb.HttpClient(host='localhost', port=8001)

#get or create a collection of table like sql
collection = chroma_client.get_or_create_collection(name="company_docs")
embedding_model = get_embedding_model("default")


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


RAG_TOOL_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "search_company_docs",
            "description": "Search the company knowledge base, uploaded documents, policies, service plans, pricing, products, and rules in ChromaDB.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query or keywords to look up in company documents"}
                },
                "required": ["query"]
            }
        }
    }
]


PREDICTION_TOOL_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "get_plant_predictions",
            "description": "Get the current predicted Permeate Flow and TDS based on live sensor data.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]



def send_email(to_address: str, subject: str, body: str):
    """A mock function to send an email and write it to a log file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] To: {to_address} | Subject: {subject} | Body: {body}\n"
    
    # Write to a file in the backend folder
    with open("sent_emails.log", "a", encoding="utf-8") as f:
        f.write(log_entry)
        
    return f"Email successfully sent to {to_address}."



def search_company_docs(query: str):
    """Hybrid Search: Combines Semantic (ChromaDB) and Keyword (Postgres) results."""
    try:
        live_col = chroma_client.get_or_create_collection(name="company_docs")
        
        # 1. Semantic Search (ChromaDB)
        vector_docs = []
        if live_col.count() > 0:
            active_model = get_embedding_model()
            query_embedding = active_model.encode(query).tolist()
            results = live_col.query(query_embeddings=[query_embedding], n_results=3)
            if results['documents'] and results['documents'][0]:
                vector_docs = results['documents'][0]

        # 2. Keyword Search (Postgres)
        keyword_docs = keyword_search_chunks(query, limit=2)

        # 3. Merge and Deduplicate
        combined_docs = list(set(vector_docs + keyword_docs))

        if not combined_docs:
            return "No relevant documents found."

        formatted_results = "\n---\n".join(combined_docs)
        return f"Found these relevant sections in the company documents:\n\n{formatted_results}"

    except Exception as e:
        raise ValueError(f"Failed to search docs: {str(e)}")



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


def get_plant_predictions():
    """Runs the ML models on live Modbus data and returns the current plant status."""
    result = predict_live_status()
    if result["status"] == "error":
        return f"Error: {result['message']}"
    
    preds = result["predictions"]
    flow = preds["alpha"]["flow"]
    tds = preds["beta"]["tds"]
    quality = preds["beta"]["quality_status"]
    
    return f"Live Plant Status:\n- Predicted Permeate Flow: {flow} m3/h\n- Predicted Permeate TDS: {tds} ppm\n- Water Quality: {quality}"



TOOL_FUNCTION = {
    "get_weather": get_weather,
    "get_all_users": get_all_users,
    "delete_user": delete_user,
    "send_email": send_email,
    "search_company_docs": search_company_docs,
    "get_plant_predictions": get_plant_predictions
}
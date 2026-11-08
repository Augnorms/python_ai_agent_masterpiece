import os
from openai import OpenAI
from dotenv import load_dotenv

# Ensure .env is loaded from backend directory even if started from another working directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))
load_dotenv()

api_key = os.getenv("grok_api_key") or os.getenv("GROK_API_KEY") or "dummy_key"

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1",
)
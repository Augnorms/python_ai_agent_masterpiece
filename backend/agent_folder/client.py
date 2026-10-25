import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("grok_api_key"),
    base_url="https://api.groq.com/openai/v1",
)
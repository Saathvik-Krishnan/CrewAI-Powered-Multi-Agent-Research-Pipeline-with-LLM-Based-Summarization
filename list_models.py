import os
from dotenv import load_dotenv
from google import genai

load_dotenv()  # loads .env into environment variables

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

for m in client.models.list():
    print(m.name, getattr(m, "supported_actions", None))

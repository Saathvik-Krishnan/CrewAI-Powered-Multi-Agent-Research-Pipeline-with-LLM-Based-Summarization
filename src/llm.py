import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = os.getenv("GEMINI_MODEL", "models/gemini-flash-latest")

def llm(prompt: str, model: str = MODEL) -> str:
    resp = client.models.generate_content(
        model=model,
        contents=prompt,
    )
    return resp.text

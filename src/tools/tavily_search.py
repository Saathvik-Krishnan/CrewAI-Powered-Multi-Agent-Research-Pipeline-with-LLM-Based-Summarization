import os
from tavily import TavilyClient
from dotenv import load_dotenv
from pathlib import Path

# Load .env from project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY not found in .env")

client = TavilyClient(api_key=TAVILY_API_KEY)

def tavily_web_search(query: str, max_results: int = 5):
    """
    AI-friendly web search using Tavily (FREE).
    Returns list of sources with content.
    """
    response = client.search(
        query=query,
        search_depth="basic",
        max_results=max_results
    )

    results = []
    for r in response.get("results", []):
        results.append({
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "content": r.get("content", "")
        })

    return results

import os
from dotenv import load_dotenv
from crewai import Agent

load_dotenv()

MODEL = os.getenv("GEMINI_MODEL", "gemini/gemini-flash-latest")

def build_research_agent():
    return Agent(
        role="Research Agent",
        goal="Turn Tavily results into a clean evidence pack with sources.",
        backstory="You are careful and cite sources. You do not invent facts.",
        verbose=True,
        llm=MODEL,
    )

def build_summary_agent():
    return Agent(
        role="Summary Agent",
        goal="Write an executive summary ONLY from the evidence.Output must be strictly markdown and the source links should also be present",
        backstory="You summarize clearly and never hallucinate.",
        verbose=True,
        llm=MODEL,
    )

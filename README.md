# CrewAI-Powered-Multi-Agent-Research-Pipeline-with-LLM-Based-Summarization

## Project Overview

This project is an end-to-end **AI-powered research assistant** that uses **multi-agent collaboration** to gather evidence from the web, validate sources, and generate an **executive-level summary**.
It demonstrates how **agentic AI workflows** can autonomously research, reason, and synthesize information using modern large language models.

The system supports both:

* A **Command-Line Interface (CLI)** workflow
* An **Interactive Web Interface** built with Streamlit

---

## Key Features

* Automated web research using **Tavily Search API**
* Multi-agent orchestration using **CrewAI**
* **Research Agent** for evidence collection and validation
* **Summary Agent** for executive summary generation (strictly evidence-based)
* **Google Gemini LLM** integration via LiteLLM
* Interactive frontend using **Streamlit**
* Markdown-style reports saved locally
* Persistent local memory storage (JSON)

---

## System Architecture (High-Level Flow)

User Input
→ Streamlit UI or CLI
→ CrewAI Orchestrator
→ Research Agent (collects & validates evidence)
→ Summary Agent (generates executive summary)
→ Outputs saved locally (report + memory)

---

## Tech Stack

### Frontend

* Streamlit

### Backend & Orchestration

* Python 3.10+
* CrewAI
* LiteLLM

### LLM & APIs

* Google Gemini API
* Tavily Search API

### Storage

* Local Markdown reports
* Local JSON memory files

---

## Project Structure

```
AI_agent_proj
├── src
│   ├── main.py              – CLI pipeline runner
│   ├── agents.py            – CrewAI agent definitions
│   ├── tasks.py             – Task definitions
│   ├── config.py            – Environment & model configuration
│
├── app.py                   – Streamlit web application
├── outputs
│   └── report.md            – Generated research reports
├── memory
│   └── memory.json          – Persistent agent memory
│
├── requirements.txt
├── .env.sample
└── README.md
```

---

## Environment Setup

### Step 1: Create a Virtual Environment

python -m venv .venv

Activate it:

**Windows**
.venv\Scripts\activate

**macOS / Linux**
source .venv/bin/activate

---

### Step 2: Install Dependencies

pip install -r requirements.txt

---

### Step 3: Configure Environment Variables

Create a `.env` file using the following template:

GEMINI_API_KEY="YOUR GEMINI API KEY"
GEMINI_MODEL=gemini/gemini-flash-latest
TAVILY_API_KEY="YOUR TAVILY API KEY"

---

## How to Run the Project

### Option 1: Command-Line Interface (CLI)

python -m src.main

* Prompts the user to enter a research topic
* Runs the multi-agent pipeline
* Saves the final report in the `outputs` folder

---

### Option 2: Web Interface (Recommended)

streamlit run app.py

* Launches a browser-based UI
* Accepts topic input interactively
* Displays execution logs and results in real time


## API Quota Notes

* Google Gemini free tier has **daily request limits**
* Multi-agent pipelines can reach the quota quickly
* To avoid issues:

  * Avoid repeated rapid executions
  * Reuse generated outputs when possible
  * Enable billing for higher limits (optional)




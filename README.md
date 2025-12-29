
#  CrewAI-Powered-Multi-Agent-Research-Pipeline-with-LLM-Based-Summarization

A Python-based multi-agent AI system that performs **source-grounded research and executive summarization** using autonomous agents. The system retrieves real-time web evidence, validates it, and generates a structured executive summary with citations.

---

##  Project Overview

This project demonstrates how **multiple AI agents** can collaborate to complete a research task end-to-end:

1. **Research Agent**

   * Gathers and validates evidence from real-world sources using web search
   * Ensures factual accuracy and source attribution

2. **Summary Agent**

   * Produces an executive summary strictly based on the collected evidence
   * Avoids hallucination by design

The system runs locally in VS Code and produces:

* A **Markdown research report**
* A **persistent memory file** for future runs

---

##  Architecture (High Level)

```
User Input
   ↓
Python Orchestrator (main.py)
   ↓
CrewAI (Multi-Agent Execution)
   ├── Research Agent → Tavily Search API
   └── Summary Agent → Google Gemini (via LiteLLM)
   ↓
Outputs (Markdown Report)
Memory (JSON)
```

---

##  Tech Stack

### Core Language

* **Python 3.11**

### AI & Agents

* **CrewAI** – Multi-agent orchestration
* **Google Gemini (Flash / 2.x)** – LLM for reasoning and summarization
* **LiteLLM** – LLM abstraction layer

### Search & Retrieval

* **Tavily API (Free Tier)** – Real-time web search with citations

### Configuration & Environment

* **python-dotenv** – Environment variable management
* **Python venv** – Dependency isolation

### Data & Outputs

* **Markdown (`.md`)** – Final research report
* **JSON** – Persistent agent memory

### Tools

* **VS Code**
* **PowerShell (Windows)**

---

##  Project Structure

```
AI_agent_proj/
│
├── src/
│   ├── main.py              # Entry point and orchestration
│   ├── agents.py            # Research & Summary agents
│   ├── tools/
│   │   └── tavily_search.py # Tavily integration
│   └── config.py            # Environment config
│
├── outputs/
│   └── report.md            # Final generated report
│
├── memory/
│   └── memory.json          # Persistent agent memory
│
├── .env                     # API keys (not committed)
├── .env.sample              # Environment template
├── requirements.txt
└── README.md
```

---

##  Setup Instructions

### 1. Clone the Repository

```bash
git clone <repo-url>
cd AI_agent_proj
```

### 2. Create & Activate Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

##  Environment Configuration

### `.env.sample` (add this file to the repo)

Create a file named **`.env.sample`** with the following contents:

```env
GEMINI_API_KEY="YOUR GEMINI API KEY"
GEMINI_MODEL=gemini/gemini-flash-latest
TAVILY_API_KEY="YOUR TAVILY API KEY"
```

### `.env` (local only)

Copy `.env.sample` → `.env` and replace the values with your actual keys.

>  **Do not commit `.env`** — it contains sensitive credentials.

---

##  How to Run

```bash
python -m src.main
```

You will be prompted to enter a research topic:

```
Enter a topic to research: AI agents in supply chain management
```

---

##  Output

After execution:

*  **Research report** → `outputs/report.md`
*  **Memory file** → `memory/memory.json`

Both agents must complete successfully for the report to be generated.

---

##  Key Design Decisions

* No traditional backend server (FastAPI/Flask not required)
* Python acts as the orchestration backend
* Emphasis on **source-grounded AI** (no hallucinations)
* Modular agent design for easy extensibility

---

##  Possible Extensions

* Add FastAPI to expose the system as a REST API
* Store memory in a database (Postgres / MongoDB)
* Add a frontend (React / Streamlit)
* Add more specialized agents (Fact Checker, Risk Analyzer)

---

##  License

This project is for **educational and evaluation purposes**.

---



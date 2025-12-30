import os
import subprocess
from pathlib import Path
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# -----------------------
# Page config
# -----------------------
st.set_page_config(
    page_title="Agentic Research Report Generator",
    page_icon="🧠",
    layout="wide",
)

# -----------------------
# Custom CSS (clean + professional)
# -----------------------
st.markdown(
    """
    <style>
      /* overall */
      .block-container { padding-top: 1.2rem; padding-bottom: 2.5rem; max-width: 1200px; }
      h1, h2, h3 { letter-spacing: -0.02em; }
      .muted { color: rgba(255,255,255,0.70); font-size: 0.95rem; }
      .small { font-size: 0.9rem; color: rgba(255,255,255,0.75); }

      /* cards */
      .card {
        border: 1px solid rgba(255,255,255,0.10);
        background: rgba(255,255,255,0.03);
        border-radius: 16px;
        padding: 16px 16px;
        margin-bottom: 14px;
      }
      .card-title { font-weight: 650; font-size: 1.05rem; margin-bottom: 6px; }
      .pill {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 999px;
        border: 1px solid rgba(255,255,255,0.12);
        background: rgba(255,255,255,0.04);
        margin-right: 8px;
        margin-bottom: 8px;
        font-size: 0.85rem;
        color: rgba(255,255,255,0.85);
      }

      /* nice buttons */
      .stDownloadButton button, .stButton button {
        border-radius: 12px !important;
        height: 44px;
        font-weight: 600;
      }

      /* text input */
      .stTextInput input {
        border-radius: 12px !important;
        height: 46px;
      }

      /* code box rounded */
      div[data-testid="stCodeBlock"] { border-radius: 14px; }
      div[data-testid="stMarkdownContainer"] a { text-decoration: none; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------
# Helpers
# -----------------------
OUTPUT_REPORT = Path("outputs") / "report.md"
MEMORY_FILE = Path("memory") / "memory.json"

def env_status():
    return {
        "TAVILY_API_KEY": bool(os.getenv("TAVILY_API_KEY")),
        "GEMINI_API_KEY": bool(os.getenv("GEMINI_API_KEY")),
        "GEMINI_MODEL": os.getenv("GEMINI_MODEL", "gemini/gemini-flash-latest"),
    }

def run_pipeline(user_topic: str):
    """
    Runs your existing CLI pipeline: python -m src.main
    and feeds the topic via stdin.
    """
    cmd = ["python", "-X", "utf8", "-m", "src.main"]

    p = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,             
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


    

    assert p.stdin is not None
    p.stdin.write(user_topic + "\n")
    p.stdin.flush()
    p.stdin.close()

    logs = []
    assert p.stdout is not None
    for line in p.stdout:
        logs.append(line)

    p.wait()
    return p.returncode, "".join(logs)

# -----------------------
# Sidebar (Configuration)
# -----------------------
st.sidebar.markdown("## ⚙️ Configuration")

status = env_status()

st.sidebar.markdown(
    f"""
<div class="card">
  <div class="card-title">Environment</div>
  <div class="small">Tavily Key: {"✅ Set" if status["TAVILY_API_KEY"] else "❌ Missing"}</div>
  <div class="small">Gemini Key: {"✅ Set" if status["GEMINI_API_KEY"] else "❌ Missing"}</div>
  <div class="small">Model: <code>{status["GEMINI_MODEL"]}</code></div>
</div>
""",
    unsafe_allow_html=True,
)

st.sidebar.markdown(
    """
<div class="card">
  <div class="card-title">What this app does</div>
  <div class="small">
    1) Takes a topic<br/>
    2) Uses Tavily to gather sources<br/>
    3) Uses Gemini to structure evidence + write an executive summary<br/>
    4) Saves a Markdown report to <code>outputs/report.md</code>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.sidebar.markdown("---")
show_logs_default = st.sidebar.toggle("Show run logs by default", value=True)
auto_open_report = st.sidebar.toggle("Auto-open report after run", value=True)

# -----------------------
# Header
# -----------------------
st.markdown("# 🧠 CrewAI-Powered-Multi-Agent-Research-Pipeline-with-LLM-Based-Summarization")
st.markdown(
    """
Generate a **cited evidence pack + executive summary** in clean **Markdown** using a multi-agent CrewAI workflow.
""",
)

# Top info pills
st.markdown(
    """
<div style="margin-top:6px; margin-bottom:8px;">
  <span class="pill">CrewAI</span>
  <span class="pill">Tavily Search</span>
  <span class="pill">Google Gemini</span>
  <span class="pill">Markdown Report</span>
</div>
""",
    unsafe_allow_html=True,
)

# -----------------------
# Project details (Markdown style)
# -----------------------
with st.expander("📌 Project details (Markdown style)", expanded=True):
    st.markdown(
        """
## Overview
This project is a **research automation tool** that converts web evidence into a structured, **source-cited** report.

## Tech Stack
- **Language:** Python
- **Agents/Orchestration:** CrewAI
- **Web Research Tooling:** Tavily API
- **LLM Provider:** Google Gemini (via `google-genai`)
- **Frontend:** Streamlit (interactive UI)
- **Output:** Markdown report (`outputs/report.md`)

## Backend
The “backend” is the Python pipeline that:
1. calls Tavily to collect sources  
2. uses Gemini to clean/structure the evidence  
3. generates an executive summary strictly from evidence  
4. writes the final Markdown report to disk
"""
    )

# -----------------------
# Main input + run
# -----------------------
colA, colB = st.columns([2.1, 1])

with colA:
    topic = st.text_input(
        "Topic to research",
        placeholder="e.g., AI agents in supply chain management",
    )

with colB:
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    run_btn = st.button("Run Research", type="primary", use_container_width=True)

# -----------------------
# Output sections
# -----------------------
log_container = st.container()
result_container = st.container()

if run_btn:
    if not topic.strip():
        st.error("Please enter a topic.")
    elif not status["TAVILY_API_KEY"] or not status["GEMINI_API_KEY"]:
        st.error("Missing API keys. Add them in your .env (or environment variables) and try again.")
    else:
        start_time = datetime.now()

        with st.spinner("Running agents… (this may take a bit depending on the topic)"):
            code, logs = run_pipeline(topic.strip())

        elapsed = (datetime.now() - start_time).total_seconds()

        # Run summary card
        st.markdown(
            f"""
<div class="card">
  <div class="card-title">Run Summary</div>
  <div class="small"><b>Topic:</b> {topic.strip()}</div>
  <div class="small"><b>Status:</b> {"✅ Completed" if code == 0 else "❌ Failed"}</div>
  <div class="small"><b>Time:</b> {elapsed:.1f}s</div>
  <div class="small"><b>Output:</b> <code>{OUTPUT_REPORT.as_posix()}</code></div>
</div>
""",
            unsafe_allow_html=True,
        )

        # Logs
        with log_container:
            show_logs = show_logs_default
            if code != 0:
                show_logs = True  # force show logs on failure

            if show_logs:
                with st.expander("🧾 Run logs", expanded=(code != 0)):
                    st.code(logs[-12000:] if len(logs) > 12000 else logs, language="text")

        # Report
        with result_container:
            if code == 0 and OUTPUT_REPORT.exists():
                report_md = OUTPUT_REPORT.read_text(encoding="utf-8")

                if auto_open_report:
                    st.markdown("## ✅ Generated Report (Markdown Preview)")
                    st.markdown(report_md)

                c1, c2, c3 = st.columns([1, 1, 2])
                with c1:
                    st.download_button(
                        "Download report.md",
                        data=report_md,
                        file_name="report.md",
                        mime="text/markdown",
                        use_container_width=True,
                    )

                with c2:
                    # Optional: download memory.json if present
                    if MEMORY_FILE.exists():
                        st.download_button(
                            "Download memory.json",
                            data=MEMORY_FILE.read_text(encoding="utf-8"),
                            file_name="memory.json",
                            mime="application/json",
                            use_container_width=True,
                        )

                with c3:
                    st.markdown(
                        "<div class='small'>Tip: Commit <code>outputs/report.md</code> into GitHub as your generated deliverable.</div>",
                        unsafe_allow_html=True,
                    )

            else:
                st.warning("No report found. If the run failed, expand logs above and share the last 30–50 lines.")

# -----------------------
# Footer
# -----------------------
st.markdown("---")
st.markdown(
    "<div class='small'>Built with Streamlit • Evidence from Tavily • Summaries from Gemini • Orchestrated via CrewAI</div>",
    unsafe_allow_html=True,
)

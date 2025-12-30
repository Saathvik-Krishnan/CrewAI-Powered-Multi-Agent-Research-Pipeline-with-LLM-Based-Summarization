import os
from crewai import Crew, Task
from src.tools.tavily_search import tavily_web_search
from src.guardrails.safety import is_unsafe, safety_message
from src.llm import llm
from src.memory_store import save_memory
from src.agents import build_research_agent, build_summary_agent
from datetime import datetime

import sys

# Force UTF-8 output in Windows terminals (prevents emoji crash)
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def build_evidence(topic: str) -> str:
    sources = tavily_web_search(topic, max_results=5)

    evidence_blocks = []
    for s in sources:
        title = s.get("title", "")
        url = s.get("url", "")
        content = s.get("content", "")

        evidence_blocks.append(
            f"## {title}\nURL: {url}\nRAW CONTENT:\n{content}\n"
        )

    return "\n".join(evidence_blocks)


def save_report(topic: str, summary: str):
    os.makedirs("outputs", exist_ok=True)
    path = os.path.join("outputs", "report.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# Topic\n{topic}\n\n# Executive Summary\n{summary}\n")
    return path

def main():
    topic = input("Enter a topic to research: ").strip()

    # Guardrails
    if is_unsafe(topic):
        print(safety_message())
        return

    print("\n[1/3] Research Agent gathering evidence using Tavily...\n")
    evidence = build_evidence(topic)

    research_agent = build_research_agent()
    summary_agent = build_summary_agent()

    t1 = Task(
        description=f"Organize and validate this evidence about: {topic}\n\nEVIDENCE:\n{evidence}.\n\nThe current date and time is: {current_time}.",
        expected_output="A cleaned evidence pack with sources.",
        agent=research_agent
    )

    t2 = Task(
        description=(
            "Write an executive summary using ONLY the evidence.\n"
            "Structure:\n1) Overview\n2) Key Findings\n3) Risks/Limitations\n4) Sources\n\n"
            f"EVIDENCE:\n{evidence}.\n\nThe current date and time is: {current_time}."
        ),
        expected_output="Executive summary with sources.",
        agent=summary_agent
    )

    print("\n[2/3] Running multi-agent crew (2 agents)...\n")
    crew = Crew(agents=[research_agent, summary_agent], tasks=[t1, t2], verbose=True)
    result = crew.kickoff()

    summary = str(result)
    report_path = save_report(topic, summary)

    save_memory({
        "topic": topic,
        "report_path": report_path,
        "summary_preview": summary[:1200]
    })

    print("\n[3/3] Done ")
    print(f"Report saved: {report_path}")
    print("Memory saved: memory/memory.json")

if __name__ == "__main__":
    main()

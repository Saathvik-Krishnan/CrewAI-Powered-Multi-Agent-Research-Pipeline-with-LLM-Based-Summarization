from src.tools.tavily_search import tavily_web_search

results = tavily_web_search("AI agents in enterprises", max_results=3)

for i, r in enumerate(results, 1):
    print(f"\n{i}. {r['title']}")
    print(r["url"])
    print(r["content"][:200], "...")

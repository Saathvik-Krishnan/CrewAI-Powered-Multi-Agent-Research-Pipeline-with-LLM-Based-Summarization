import json
import os
from datetime import datetime

MEM_PATH = os.path.join("memory", "memory.json")

def load_memory():
    if not os.path.exists(MEM_PATH):
        return []
    with open(MEM_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memory(entry: dict):
    os.makedirs("memory", exist_ok=True)
    data = load_memory()
    entry["timestamp"] = datetime.now().isoformat(timespec="seconds")
    data.append(entry)
    with open(MEM_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

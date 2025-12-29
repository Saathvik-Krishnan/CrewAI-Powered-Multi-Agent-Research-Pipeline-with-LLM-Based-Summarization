def is_unsafe(user_text: str) -> bool:
    bad = [
        "hack", "phishing", "steal password", "exploit", "malware",
        "bomb", "weapon", "kill", "dox", "ssn", "credit card"
    ]
    t = user_text.lower()
    return any(k in t for k in bad)

def safety_message() -> str:
    return "Blocked by safety rules. Please ask a safe, legal research question."

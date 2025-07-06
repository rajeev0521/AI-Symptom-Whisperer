CRISIS_KEYWORDS = {
    "high": [
        "kill myself", "suicide", "end my life", "not worth living", "better off dead",
        "suicide plan", "kill me", "die", "ending it all", "can't go on"
    ],
    "medium": [
        "hopeless", "worthless", "pointless", "give up", "can't take it anymore",
        "want to disappear", "tired of living", "nothing matters", "no point"
    ],
    "self_harm": [
        "cut myself", "hurt myself", "self harm", "cutting", "burning myself",
        "punish myself", "deserve pain", "physical pain"
    ]
}

def detect_crisis_level(text: str) -> str:
    text_lower = text.lower()
    for keyword in CRISIS_KEYWORDS["high"] + CRISIS_KEYWORDS["self_harm"]:
        if keyword in text_lower:
            return "high"
    for keyword in CRISIS_KEYWORDS["medium"]:
        if keyword in text_lower:
            return "medium"
    return "none"

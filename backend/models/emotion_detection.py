from enum import Enum

class EmotionalState(Enum):
    NEUTRAL = "neutral"
    ANXIOUS = "anxious"
    DEPRESSED = "depressed"
    ANGRY = "angry"
    OVERWHELMED = "overwhelmed"
    HOPEFUL = "hopeful"
    CRISIS = "crisis"

def detect_emotional_state(text: str) -> EmotionalState:
    text_lower = text.lower()
    if any(word in text_lower for word in ["anxious", "worried", "nervous", "panic", "fear"]):
        return EmotionalState.ANXIOUS
    if any(word in text_lower for word in ["sad", "depressed", "hopeless", "worthless", "empty"]):
        return EmotionalState.DEPRESSED
    if any(word in text_lower for word in ["angry", "furious", "mad", "frustrated", "rage"]):
        return EmotionalState.ANGRY
    if any(word in text_lower for word in ["overwhelmed", "too much", "can't handle", "drowning"]):
        return EmotionalState.OVERWHELMED
    if any(word in text_lower for word in ["hope", "better", "improving", "optimistic"]):
        return EmotionalState.HOPEFUL
    return EmotionalState.NEUTRAL

import subprocess
from utils.therapy_prompts import TherapyPrompts, EmotionalState, TherapyApproach, detect_crisis_level

def detect_emotion(user_input):
    # Simple keyword-based detection (replace with your advanced logic if available)
    if any(word in user_input.lower() for word in ["anxious", "worried", "nervous"]):
        return EmotionalState.ANXIOUS
    if any(word in user_input.lower() for word in ["sad", "depressed", "hopeless"]):
        return EmotionalState.DEPRESSED
    if any(word in user_input.lower() for word in ["angry", "mad", "frustrated"]):
        return EmotionalState.ANGRY
    if any(word in user_input.lower() for word in ["overwhelmed", "too much", "can't handle"]):
        return EmotionalState.OVERWHELMED
    if any(word in user_input.lower() for word in ["hope", "better", "improving"]):
        return EmotionalState.HOPEFUL
    return EmotionalState.NEUTRAL

def main():
    model_name = "llama3.1:8b-instruct-q4_0"
    therapy_prompts = TherapyPrompts()
    session_history = []

    print("Welcome to the AI Mental Health Counselor. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ["exit", "quit"]:
            print("Session ended. Take care!")
            break

        # Detect emotion and crisis
        emotion = detect_emotion(user_input)
        crisis_level = detect_crisis_level(user_input)
        approach = TherapyApproach.CBT  # You can make this dynamic

        # Build prompt using your TherapyPrompts logic
        prompt = therapy_prompts.build_contextual_prompt(
            base_context=f"User just said: '{user_input}'",
            emotional_state=emotion,
            therapy_approach=approach,
            session_history=session_history,
            crisis_indicators=(crisis_level in ["high", "medium"])
        )

        # Call Ollama CLI
        result = subprocess.run(
            ["ollama", "run", model_name],
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=120
        )
        if result.returncode == 0:
            ai_response = result.stdout.strip()
            print(f"Alex: {ai_response}\n")
            session_history.append(f"User: {user_input}\nAlex: {ai_response}")
        else:
            print(f"Error: {result.stderr.strip()}\n")

if __name__ == "__main__":
    main() 
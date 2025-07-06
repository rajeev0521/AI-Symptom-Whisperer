class VoiceService:
    """
    Stub for voice input/output. Extend with speech-to-text and text-to-speech as needed.
    """
    def transcribe_audio(self, audio_bytes: bytes) -> str:
        # Placeholder: integrate with a speech-to-text API
        return "Transcribed text from audio."

    def synthesize_speech(self, text: str) -> bytes:
        # Placeholder: integrate with a text-to-speech API
        return b"Audio bytes for synthesized speech."

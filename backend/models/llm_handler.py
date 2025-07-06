import subprocess
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class LLMHandler:
    """
    Handles communication with the Llama 3.1 LLM via local Ollama CLI.
    """
    def __init__(self, model_name: str = "llama3.1:8b-instruct-q4_0"):
        self.model_name = model_name

    def generate(self, prompt: str, options: Optional[Dict[str, Any]] = None, timeout: int = 60) -> str:
        """
        Generate a response from the LLM using the local Ollama CLI.

        Args:
            prompt: The prompt to send to the LLM.
            options: (Unused, for compatibility)
            timeout: Max time to wait for a response.
        Returns:
            The generated response as a string.
        """
        try:
            # Build the command for ollama
            cmd = [
                "ollama", "run", self.model_name,
                "--prompt", prompt
            ]
            # Run the command and capture output
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                logger.error(f"Ollama CLI error: {result.stderr}")
                return "I'm having trouble generating a response right now. Please try again."
        except subprocess.TimeoutExpired:
            logger.error("Ollama CLI timed out.")
            return "I'm unable to generate a response in time. Please try again later."
        except Exception as e:
            logger.error(f"Ollama CLI error: {e}")
            return "I'm unable to connect to my language model right now. Please try again later."

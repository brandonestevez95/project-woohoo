import ollama
from typing import Optional

class ScriptGenerator:
    """Generate podcast scripts using Claude via Ollama."""

    def __init__(self, model: str = "claude"):
        self.model = model
        try:
            ollama.pull(model)
        except Exception as e:
            print(f"Warning: could not pull model {model}: {e}")

    def generate(self, text: str, prompt: str) -> str:
        """Generate a script given source text and a dynamic prompt."""
        messages = [
            {"role": "system", "content": "You create podcast scripts from academic sources."},
            {"role": "user", "content": f"{prompt}\n\n{text}"},
        ]
        try:
            response = ollama.chat(model=self.model, messages=messages)
            return response["message"]["content"]
        except Exception as e:
            print(f"Error generating script: {e}")
            return ""

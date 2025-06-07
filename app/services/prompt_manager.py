from typing import Dict

class PromptManager:
    """Build prompts for different learning arcs and tones."""

    _ARCS: Dict[str, str] = {
        "Civic Storyteller": "You craft narratives that connect civic themes with everyday life.",
        "Youth Science Explainer": "You explain scientific concepts to a young audience in an accessible way.",
    }

    def build_prompt(self, arc: str, tone: str) -> str:
        base = self._ARCS.get(arc, "You create engaging educational podcasts.")
        return (
            f"{base}\n"
            f"Tone: {tone}.\n"
            "Structure the script with an introduction, key ideas, example, and outro."
        )

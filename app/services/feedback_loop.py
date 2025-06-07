import json
from pathlib import Path
from typing import Dict, List

class FeedbackLoop:
    """Store user feedback for episodes."""

    def __init__(self, feedback_file: str = "output/feedback.json"):
        self.feedback_path = Path(feedback_file)
        self.feedback_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.feedback_path.exists():
            self._save([])

    def _load(self) -> List[Dict]:
        try:
            with open(self.feedback_path) as f:
                return json.load(f)
        except Exception:
            return []

    def _save(self, data: List[Dict]):
        with open(self.feedback_path, "w") as f:
            json.dump(data, f, indent=2)

    def add_feedback(self, episode_id: str, rating: int, notes: str = ""):
        feedback = self._load()
        feedback.append({"episode_id": episode_id, "rating": rating, "notes": notes})
        self._save(feedback)

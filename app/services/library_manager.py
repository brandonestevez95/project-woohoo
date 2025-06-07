import json
from pathlib import Path
from typing import Dict, List

class LibraryManager:
    """Manage stored podcast episodes and metadata."""

    def __init__(self, index_file: str = "output/episode_index.json"):
        self.index_path = Path(index_file)
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.index_path.exists():
            self._save([])

    def _load(self) -> List[Dict]:
        try:
            with open(self.index_path) as f:
                return json.load(f)
        except Exception:
            return []

    def _save(self, episodes: List[Dict]):
        with open(self.index_path, "w") as f:
            json.dump(episodes, f, indent=2)

    def add_episode(self, episode: Dict):
        episodes = self._load()
        episodes.append(episode)
        self._save(episodes)

    def list_episodes(self) -> List[Dict]:
        return self._load()

    def search(self, query: str) -> List[Dict]:
        query = query.lower()
        return [e for e in self._load() if query in e.get("title", "").lower() or any(query in t.lower() for t in e.get("tags", []))]

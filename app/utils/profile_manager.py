import json
from pathlib import Path
from typing import Dict, List, Optional
import time
import uuid
from datetime import datetime

class ProfileManager:
    def __init__(self, data_dir: str = "data"):
        """Initialize profile manager with predefined learning arcs and topics."""
        self.data_dir = Path(data_dir)
        self.profiles_dir = self.data_dir / "profiles"
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
        
        self.profiles = {}
        self._interests = [
            "Artificial Intelligence",
            "Machine Learning",
            "Data Science",
            "Computer Science",
            "Software Engineering",
            "Robotics",
            "Natural Language Processing",
            "Quantum Computing",
            "Cybersecurity",
            "Cloud Computing"
        ]
        
        self._learning_arcs = [
            {
                "id": "ai_basics",
                "name": "AI Fundamentals",
                "description": "Learn the core concepts of artificial intelligence and machine learning",
                "difficulty": "Beginner",
                "topics": ["AI Basics", "Machine Learning", "Neural Networks"]
            },
            {
                "id": "data_science",
                "name": "Data Science Journey",
                "description": "Master data analysis, visualization, and statistical methods",
                "difficulty": "Intermediate",
                "topics": ["Statistics", "Data Analysis", "Python", "Data Visualization"]
            },
            {
                "id": "future_tech",
                "name": "Future Technologies",
                "description": "Explore cutting-edge technologies shaping our future",
                "difficulty": "Advanced",
                "topics": ["Quantum Computing", "Robotics", "Blockchain"]
            }
        ]

    def create_profile(
        self,
        name: str,
        interests: List[str],
        learning_arcs: List[str],
        language: str = "en",
        voice_preference: str = "default"
    ) -> str:
        """Create a new user profile."""
        profile_id = str(uuid.uuid4())
        self.profiles[profile_id] = {
            "id": profile_id,
            "name": name,
            "interests": interests,
            "learning_arcs": learning_arcs,
            "language": language,
            "voice_preference": voice_preference,
            "created_at": datetime.now().strftime("%Y-%m-%d"),
            "completed_episodes": [],
            "progress": {arc: 0 for arc in learning_arcs}
        }
        self._save_profile(profile_id, self.profiles[profile_id])
        return profile_id
    
    def get_profile(self, profile_id: str) -> Optional[Dict]:
        """Get a profile by ID."""
        return self.profiles.get(profile_id)
    
    def update_profile(self, profile_id: str, updates: Dict) -> bool:
        """Update a profile."""
        if profile_id in self.profiles:
            self.profiles[profile_id].update(updates)
            self.profiles[profile_id]["last_updated"] = time.time()
            return self._save_profile(profile_id, self.profiles[profile_id])
        return False
    
    def record_episode_completion(
        self,
        profile_id: str,
        episode_id: str,
        learning_arc: str
    ) -> bool:
        """Record completion of an episode."""
        profile = self.get_profile(profile_id)
        if not profile:
            return False
            
        if episode_id not in profile["completed_episodes"]:
            profile["completed_episodes"].append(episode_id)
            
        # Update progress in learning arc
        if learning_arc in profile["progress"]:
            profile["progress"][learning_arc] += 1
            
        return self._save_profile(profile_id, profile)
    
    def get_learning_progress(self, profile_id: str) -> Dict:
        """Get learning progress for all arcs."""
        profile = self.get_profile(profile_id)
        if not profile:
            return {}
            
        return {
            "completed_episodes": len(profile["completed_episodes"]),
            "arc_progress": profile["progress"],
            "interests": profile["interests"]
        }
    
    def _save_profile(self, profile_id: str, profile: Dict) -> bool:
        """Save profile to file."""
        try:
            profile_path = self.profiles_dir / f"{profile_id}.json"
            with open(profile_path, "w") as f:
                json.dump(profile, f, indent=2)
            return True
        except:
            return False

    @property
    def available_learning_arcs(self) -> List[Dict]:
        """Get list of available learning arcs."""
        return self._learning_arcs
    
    @property
    def available_interests(self) -> List[str]:
        """Get list of available interests."""
        return self._interests 
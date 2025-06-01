import json
from pathlib import Path
from typing import Dict, List, Optional
import uuid
from datetime import datetime

class ProfileManager:
    def __init__(self, data_dir: str = "data"):
        """Initialize profile manager with predefined interests."""
        self.data_dir = Path(data_dir)
        self.profiles_dir = self.data_dir / "profiles"
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
        
        self.profiles = {}
        self._interests = [
            # Technology & Computing
            "Artificial Intelligence",
            "Machine Learning",
            "Data Science",
            "Computer Science",
            "Software Engineering",
            "Cloud Computing",
            "Web Development",
            "Mobile Development",
            "DevOps",
            "Cybersecurity",
            
            # Science & Mathematics
            "Mathematics",
            "Physics",
            "Chemistry",
            "Biology",
            "Environmental Science",
            "Astronomy",
            "Statistics",
            
            # Arts & Humanities
            "Art History",
            "Literature",
            "Philosophy",
            "Music",
            "Film Studies",
            "Theater",
            "Creative Writing",
            
            # Design & Architecture
            "Graphic Design",
            "Industrial Design",
            "Architecture",
            "Urban Planning",
            "Interior Design",
            "UX/UI Design",
            
            # Business & Economics
            "Economics",
            "Business Management",
            "Marketing",
            "Finance",
            "Entrepreneurship",
            
            # Social Sciences
            "Psychology",
            "Sociology",
            "Anthropology",
            "Political Science",
            "Education",
            
            # Agriculture & Environment
            "Agricultural Science",
            "Sustainable Agriculture",
            "Environmental Studies",
            "Horticulture",
            "Food Science",
            
            # Health & Medicine
            "Medicine",
            "Public Health",
            "Nutrition",
            "Mental Health",
            "Sports Science"
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
            "episodes": []
        }
        self._save_profile(profile_id, self.profiles[profile_id])
        return profile_id
    
    def get_profile(self, profile_id: str) -> Optional[Dict]:
        """Get a profile by ID."""
        if profile_id not in self.profiles:
            try:
                profile_path = self.profiles_dir / f"{profile_id}.json"
                if profile_path.exists():
                    with open(profile_path, "r") as f:
                        self.profiles[profile_id] = json.load(f)
            except:
                return None
        return self.profiles.get(profile_id)
    
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
    def available_interests(self) -> List[str]:
        """Get list of available interests."""
        return self._interests 
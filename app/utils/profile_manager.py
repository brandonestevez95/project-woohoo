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

    @property
    def available_learning_arcs(self) -> List[Dict]:
        """Return predefined learning arcs for profile selection."""
        return [
            {
                "id": "ai_basics",
                "name": "AI Basics",
                "description": "Introduction to core concepts of artificial intelligence",
                "difficulty": "Beginner",
                "topics": ["history of AI", "machine learning overview", "applications"],
            },
            {
                "id": "stem",
                "name": "STEM Foundations",
                "description": "Fundamental science, technology, engineering and math topics",
                "difficulty": "Beginner",
                "topics": ["physics", "chemistry", "engineering principles"],
            },
            {
                "id": "future",
                "name": "Future Technology",
                "description": "Emerging trends and technologies shaping tomorrow",
                "difficulty": "Intermediate",
                "topics": ["AI trends", "space exploration", "biotechnology"],
            },
            {
                "id": "sustainability",
                "name": "Sustainability",
                "description": "Environmental responsibility and sustainable practices",
                "difficulty": "Intermediate",
                "topics": ["renewable energy", "climate change", "green tech"],
            },
        ]

    def update_profile(self, profile_id: str, updates: Dict) -> bool:
        """Update an existing profile with provided values."""
        profile = self.get_profile(profile_id)
        if not profile:
            return False
        profile.update(updates)
        profile["last_updated"] = datetime.now().strftime("%Y-%m-%d")
        self.profiles[profile_id] = profile
        return self._save_profile(profile_id, profile)

import json
from pathlib import Path
from typing import Dict, List, Optional
import time

class ProfileManager:
    def __init__(self, data_dir: str = "data"):
        """Initialize profile manager."""
        self.data_dir = Path(data_dir)
        self.profiles_dir = self.data_dir / "profiles"
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
        
    def create_profile(
        self,
        name: str,
        interests: List[str],
        learning_arcs: List[str],
        language: str = "en",
        voice_preference: str = "default"
    ) -> str:
        """Create a new user profile."""
        profile_id = str(int(time.time()))
        profile = {
            "id": profile_id,
            "name": name,
            "interests": interests,
            "learning_arcs": learning_arcs,
            "language": language,
            "voice_preference": voice_preference,
            "completed_episodes": [],
            "progress": {arc: 0 for arc in learning_arcs},
            "created_at": time.time(),
            "last_updated": time.time()
        }
        
        self._save_profile(profile_id, profile)
        return profile_id
    
    def get_profile(self, profile_id: str) -> Optional[Dict]:
        """Get a profile by ID."""
        profile_path = self.profiles_dir / f"{profile_id}.json"
        if not profile_path.exists():
            return None
            
        try:
            with open(profile_path) as f:
                return json.load(f)
        except:
            return None
    
    def update_profile(self, profile_id: str, updates: Dict) -> bool:
        """Update a profile with new data."""
        profile = self.get_profile(profile_id)
        if not profile:
            return False
            
        profile.update(updates)
        profile["last_updated"] = time.time()
        return self._save_profile(profile_id, profile)
    
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
        return [
            {
                "id": "stem",
                "name": "STEM Exploration",
                "description": "Dive into cutting-edge science and technology",
                "long_description": """Explore the frontiers of science, technology, engineering, and mathematics. 
                This learning path covers breakthrough research, emerging technologies, and fundamental concepts
                that shape our understanding of the world.""",
                "topics": [
                    "Quantum Computing",
                    "AI & Machine Learning",
                    "Biotechnology",
                    "Space Exploration",
                    "Renewable Energy",
                    "Data Science"
                ],
                "recommended_sources": [
                    "arXiv preprints",
                    "Nature journal",
                    "MIT Technology Review"
                ],
                "difficulty": "Intermediate"
            },
            {
                "id": "civic",
                "name": "Civic Innovation",
                "description": "Reimagine cities and communities for the future",
                "long_description": """Discover how urban planning, policy innovation, and community engagement 
                are shaping the cities of tomorrow. Learn about sustainable development, smart city initiatives,
                and the intersection of technology and civic life.""",
                "topics": [
                    "Smart Cities",
                    "Urban Planning",
                    "Public Policy",
                    "Civic Technology",
                    "Community Design",
                    "Sustainability"
                ],
                "recommended_sources": [
                    "CityLab",
                    "Urban Studies journals",
                    "Policy research papers"
                ],
                "difficulty": "Intermediate"
            },
            {
                "id": "humanities",
                "name": "Digital Humanities",
                "description": "Where technology meets cultural understanding",
                "long_description": """Explore how digital tools and AI are transforming our understanding of 
                history, literature, and culture. Learn about computational approaches to humanities research
                and the preservation of cultural heritage.""",
                "topics": [
                    "Digital Archives",
                    "Cultural Analytics",
                    "Literary Computing",
                    "Historical Data",
                    "Media Studies",
                    "Digital Preservation"
                ],
                "recommended_sources": [
                    "Digital Humanities Quarterly",
                    "Cultural heritage databases",
                    "Academic repositories"
                ],
                "difficulty": "Advanced"
            },
            {
                "id": "sustainability",
                "name": "Climate Action",
                "description": "Understanding and addressing climate change",
                "long_description": """Dive deep into climate science, conservation strategies, and sustainable 
                development initiatives. Learn about cutting-edge research, policy approaches, and technological
                solutions to environmental challenges.""",
                "topics": [
                    "Climate Science",
                    "Green Technology",
                    "Conservation",
                    "Environmental Policy",
                    "Sustainable Business",
                    "Renewable Resources"
                ],
                "recommended_sources": [
                    "IPCC reports",
                    "Environmental journals",
                    "Climate policy papers"
                ],
                "difficulty": "Intermediate"
            },
            {
                "id": "future",
                "name": "Future Studies",
                "description": "Exploring tomorrow's possibilities today",
                "long_description": """Investigate emerging trends, breakthrough technologies, and societal 
                shifts that will shape our future. Learn about foresight methodologies, scenario planning,
                and the intersection of technology and society.""",
                "topics": [
                    "Emerging Technologies",
                    "Social Innovation",
                    "Future of Work",
                    "Technological Ethics",
                    "Global Trends",
                    "Scenario Planning"
                ],
                "recommended_sources": [
                    "Future Studies journals",
                    "Think tank reports",
                    "Technology forecasts"
                ],
                "difficulty": "Advanced"
            }
        ]
    
    @property
    def available_interests(self) -> List[str]:
        """Get list of available interests."""
        return [
            "Artificial Intelligence",
            "Climate Change",
            "Urban Development",
            "Digital Culture",
            "Future Technology",
            "Social Impact",
            "Scientific Research",
            "Policy Innovation",
            "Data Science",
            "Sustainable Design",
            "Cultural Heritage",
            "Technology Ethics",
            "Innovation & Entrepreneurship",
            "Environmental Science",
            "Smart Cities"
        ] 
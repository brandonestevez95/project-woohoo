import json
from pathlib import Path
from typing import List, Dict, Optional
import bibtexparser
import csv
import magic
import os

class FileHandler:
    def __init__(self, output_dir: str = "output"):
        """Initialize file handler with output directory."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.index_path = self.output_dir / "episode_index.json"
        self._ensure_index()
    
    def _ensure_index(self):
        """Ensure episode index file exists."""
        if not self.index_path.exists():
            self.save_index([])
    
    def save_index(self, episodes: List[Dict]):
        """Save episode index to JSON file."""
        with open(self.index_path, "w") as f:
            json.dump(episodes, f, indent=2)
    
    def load_index(self) -> List[Dict]:
        """Load episode index from JSON file."""
        try:
            with open(self.index_path) as f:
                return json.load(f)
        except:
            return []
    
    def save_episode(
        self,
        title: str,
        script: str,
        audio_path: str,
        summary: str,
        sources: List[Dict],
        tags: List[str]
    ) -> Optional[str]:
        """Save episode files and update index."""
        try:
            # Generate unique ID
            episode_id = str(len(self.load_index()) + 1).zfill(4)
            
            # Save transcript
            transcript_path = self.output_dir / f"transcript_{episode_id}.txt"
            with open(transcript_path, "w") as f:
                f.write(script)
            
            # Update index
            episodes = self.load_index()
            episodes.append({
                "id": episode_id,
                "title": title,
                "summary": summary,
                "transcript_path": str(transcript_path),
                "audio_path": audio_path,
                "sources": sources,
                "tags": tags
            })
            self.save_index(episodes)
            
            return episode_id
        except Exception as e:
            print(f"Error saving episode: {e}")
            return None
    
    def parse_bibliography(self, file_path: str) -> List[Dict]:
        """Parse bibliography file (.bib or .csv) into source format."""
        try:
            mime = magic.Magic(mime=True)
            file_type = mime.from_file(file_path)
            
            if "text/plain" in file_type and file_path.endswith(".bib"):
                return self._parse_bibtex(file_path)
            elif "text/csv" in file_type:
                return self._parse_csv(file_path)
            else:
                print(f"Unsupported file type: {file_type}")
                return []
        except Exception as e:
            print(f"Error parsing bibliography: {e}")
            return []
    
    def _parse_bibtex(self, file_path: str) -> List[Dict]:
        """Parse BibTeX file into source format."""
        with open(file_path) as f:
            bib_database = bibtexparser.load(f)
        
        sources = []
        for entry in bib_database.entries:
            source = {
                "title": entry.get("title", ""),
                "authors": [a.strip() for a in entry.get("author", "").split(" and ")],
                "abstract": entry.get("abstract", ""),
                "tags": [entry.get("keywords", "")],
                "url": entry.get("url", ""),
                "date": entry.get("year", ""),
                "type": entry.get("ENTRYTYPE", "")
            }
            sources.append(source)
        return sources
    
    def _parse_csv(self, file_path: str) -> List[Dict]:
        """Parse CSV file into source format."""
        sources = []
        with open(file_path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                source = {
                    "title": row.get("title", ""),
                    "authors": [a.strip() for a in row.get("authors", "").split(";")],
                    "abstract": row.get("abstract", ""),
                    "tags": [t.strip() for t in row.get("tags", "").split(";")],
                    "url": row.get("url", ""),
                    "date": row.get("date", ""),
                    "type": row.get("type", "")
                }
                sources.append(source)
        return sources 
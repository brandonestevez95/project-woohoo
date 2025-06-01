from pyzotero import zotero
from typing import List, Dict, Optional
import os

class ZoteroService:
    def __init__(self, library_id: str, api_key: Optional[str] = None):
        """Initialize Zotero service with library ID and optional API key."""
        self.library_id = library_id
        self.api_key = api_key or os.getenv("ZOTERO_API_KEY")
        self.zot = zotero.Zotero(library_id, "group" if "/" in library_id else "user", self.api_key)
    
    def get_items(self, limit: int = 50) -> List[Dict]:
        """Fetch items from the Zotero library."""
        try:
            items = self.zot.top(limit=limit)
            return [self._process_item(item) for item in items]
        except Exception as e:
            print(f"Error fetching Zotero items: {e}")
            return []
    
    def _process_item(self, item: Dict) -> Dict:
        """Process a Zotero item into a standardized format."""
        data = item["data"]
        return {
            "id": data.get("key"),
            "title": data.get("title", ""),
            "authors": self._get_authors(data),
            "abstract": data.get("abstractNote", ""),
            "tags": [tag["tag"] for tag in data.get("tags", [])],
            "url": data.get("url", ""),
            "date": data.get("date", ""),
            "type": data.get("itemType", ""),
        }
    
    def _get_authors(self, data: Dict) -> List[str]:
        """Extract author names from item data."""
        creators = data.get("creators", [])
        authors = []
        for creator in creators:
            if creator.get("creatorType") == "author":
                name_parts = []
                if "firstName" in creator:
                    name_parts.append(creator["firstName"])
                if "lastName" in creator:
                    name_parts.append(creator["lastName"])
                authors.append(" ".join(name_parts))
        return authors 
from pyzotero import zotero
from typing import List, Dict, Optional
import os

class ZoteroService:
    def __init__(self, library_id: str, api_key: Optional[str] = None):
        """Initialize Zotero service with library ID and optional API key."""
        self.library_id = library_id
        self.api_key = api_key or os.getenv("ZOTERO_API_KEY")
        if not self.library_id or not self.api_key:
            raise ValueError("Both library_id and api_key are required")
        self.zot = zotero.Zotero(library_id, "group" if "/" in library_id else "user", self.api_key)
    
    def test_connection(self) -> bool:
        """Test the Zotero connection by attempting to fetch a single item."""
        try:
            self.zot.top(limit=1)
            return True
        except Exception as e:
            print(f"Zotero connection test failed: {e}")
            return False
    
    def get_collections(self) -> List[Dict]:
        """Fetch collections from the Zotero library."""
        try:
            return self.zot.collections()
        except Exception as e:
            print(f"Error fetching Zotero collections: {e}")
            return []
    
    def get_items_in_collection(self, collection_key: str) -> List[Dict]:
        """Fetch items from a specific collection."""
        try:
            return self.zot.collection_items(collection_key)
        except Exception as e:
            print(f"Error fetching collection items: {e}")
            return []
    
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
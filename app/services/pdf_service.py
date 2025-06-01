import PyPDF2
from pathlib import Path
from typing import Dict, Optional

class PDFService:
    def __init__(self):
        """Initialize the PDF service."""
        pass
        
    def extract_text(self, file_path: str) -> str:
        """Extract text from a PDF file."""
        text = []
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text.append(page.extract_text())
        return "\n\n".join(text)
        
    def get_metadata(self, file_path: str) -> Dict:
        """Extract metadata from a PDF file."""
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            metadata = reader.metadata
            
            # Clean up metadata
            clean_metadata = {
                'title': metadata.get('/Title', '').strip() if metadata.get('/Title') else None,
                'author': metadata.get('/Author', '').strip() if metadata.get('/Author') else None,
                'subject': metadata.get('/Subject', '').strip() if metadata.get('/Subject') else None,
                'keywords': metadata.get('/Keywords', '').strip() if metadata.get('/Keywords') else None,
                'creator': metadata.get('/Creator', '').strip() if metadata.get('/Creator') else None,
                'producer': metadata.get('/Producer', '').strip() if metadata.get('/Producer') else None,
                'pages': len(reader.pages)
            }
            
            # Use filename as title if no title in metadata
            if not clean_metadata['title']:
                clean_metadata['title'] = Path(file_path).stem
                
            return clean_metadata 
from PyPDF2 import PdfReader
from typing import List, Optional
import os
from pathlib import Path

class PDFService:
    def __init__(self, upload_dir: str = "uploads"):
        """Initialize PDF service with upload directory."""
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(exist_ok=True)
        
    def save_uploaded_file(self, uploaded_file) -> str:
        """Save an uploaded file and return its path."""
        file_path = self.upload_dir / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return str(file_path)
    
    def extract_text(self, file_path: str) -> str:
        """Extract text from a PDF file."""
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""
    
    def get_metadata(self, file_path: str) -> dict:
        """Get metadata from a PDF file."""
        try:
            reader = PdfReader(file_path)
            return {
                "title": reader.metadata.get("/Title", "Unknown"),
                "author": reader.metadata.get("/Author", "Unknown"),
                "subject": reader.metadata.get("/Subject", ""),
                "keywords": reader.metadata.get("/Keywords", ""),
                "creator": reader.metadata.get("/Creator", ""),
                "producer": reader.metadata.get("/Producer", ""),
                "creation_date": reader.metadata.get("/CreationDate", ""),
                "modification_date": reader.metadata.get("/ModDate", ""),
                "pages": len(reader.pages)
            }
        except Exception as e:
            print(f"Error getting PDF metadata: {e}")
            return {} 
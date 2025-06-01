from pathlib import Path
import PyPDF2
import re
from typing import Dict, List, Optional
import tempfile
import streamlit as st

class PDFProcessor:
    def __init__(self):
        """Initialize PDF processor."""
        self.temp_dir = Path(tempfile.gettempdir()) / "woohoo_uploads"
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    def process_uploaded_file(self, uploaded_file) -> Dict:
        """Process an uploaded PDF file and return extracted information."""
        try:
            # Save uploaded file to temp directory
            temp_path = self.temp_dir / uploaded_file.name
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            
            # Extract text and metadata
            with open(temp_path, "rb") as f:
                pdf = PyPDF2.PdfReader(f)
                
                # Get basic metadata
                metadata = {
                    "title": uploaded_file.name,
                    "num_pages": len(pdf.pages),
                    "file_size": uploaded_file.size,
                }
                
                # Extract text from each page
                full_text = ""
                page_texts = []
                
                for page_num, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    text = self._clean_text(text)
                    page_texts.append(text)
                    full_text += "\n" + text
                
                # Process the full text to find sections
                sections = self._extract_sections(full_text)
                
                # Clean up temp file
                temp_path.unlink()
                
                return {
                    "metadata": metadata,
                    "full_text": full_text.strip(),
                    "sections": sections
                }
                
        except Exception as e:
            st.error(f"Error processing PDF: {str(e)}")
            return None
    
    def _clean_text(self, text: str) -> str:
        """Clean extracted text by removing artifacts and normalizing spacing."""
        # Remove multiple spaces and normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove page numbers
        text = re.sub(r'\n\d+\n', '\n', text)
        text = re.sub(r'^\d+$', '', text, flags=re.MULTILINE)
        
        # Remove hyphenation at line breaks
        text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)
        
        # Fix common PDF artifacts
        text = text.replace('ﬁ', 'fi')
        text = text.replace('ﬂ', 'fl')
        text = text.replace('−', '-')
        text = text.replace('…', '...')
        
        # Normalize quotes and apostrophes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        
        # Remove excessive newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()
    
    def _extract_sections(self, text: str) -> List[Dict]:
        """Extract sections from text using improved academic paper structure detection."""
        sections = []
        
        # Common section header patterns in academic papers
        header_patterns = [
            # Standard sections
            r'^(?:(?:\d+\.)?\s*)?(?:ABSTRACT|Abstract)',
            r'^(?:(?:\d+\.)?\s*)?(?:INTRODUCTION|Introduction)',
            r'^(?:(?:\d+\.)?\s*)?(?:BACKGROUND|Background)',
            r'^(?:(?:\d+\.)?\s*)?(?:LITERATURE\s+REVIEW|Literature\s+Review)',
            r'^(?:(?:\d+\.)?\s*)?(?:METHODOLOGY|Methodology|METHODS|Methods)',
            r'^(?:(?:\d+\.)?\s*)?(?:RESULTS|Results)',
            r'^(?:(?:\d+\.)?\s*)?(?:DISCUSSION|Discussion)',
            r'^(?:(?:\d+\.)?\s*)?(?:CONCLUSION|Conclusion|CONCLUSIONS|Conclusions)',
            r'^(?:(?:\d+\.)?\s*)?(?:REFERENCES|References|BIBLIOGRAPHY|Bibliography)',
            r'^(?:(?:\d+\.)?\s*)?(?:APPENDIX|Appendix|APPENDICES|Appendices)',
            
            # Numbered sections
            r'^\d+\.\s+[A-Z][A-Za-z\s]{2,50}$',
            
            # Common academic paper subsections
            r'^(?:(?:\d+\.\d+\.)?\s*)?(?:Research Questions|Objectives|Hypotheses)',
            r'^(?:(?:\d+\.\d+\.)?\s*)?(?:Data Collection|Analysis|Findings)',
            r'^(?:(?:\d+\.\d+\.)?\s*)?(?:Theoretical Framework|Conceptual Framework)',
            r'^(?:(?:\d+\.\d+\.)?\s*)?(?:Limitations|Future Research|Implications)'
        ]
        
        # Combine patterns
        combined_pattern = '|'.join(f'({pattern})' for pattern in header_patterns)
        
        # Split text into potential sections
        parts = re.split(f'({combined_pattern})', text, flags=re.MULTILINE)
        
        current_section = {"title": "Abstract", "content": ""}
        
        for part in parts:
            if part and part.strip():
                # Check if this part matches any header pattern
                is_header = any(re.match(pattern, part.strip(), re.MULTILINE) for pattern in header_patterns)
                
                if is_header:
                    # Save previous section if it has content
                    if current_section["content"].strip():
                        sections.append(current_section)
                    current_section = {"title": part.strip(), "content": ""}
                else:
                    # Add to current section content
                    current_section["content"] += " " + part.strip()
        
        # Add the last section
        if current_section["content"].strip():
            sections.append(current_section)
        
        return sections 
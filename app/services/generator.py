from typing import List, Dict, Optional
from pathlib import Path
import time
import json
import os
import tempfile

from app.services.gpt_service import LLMService
from app.services.tts_service import TTSService
from app.utils.file_handler import FileHandler

class Generator:
    def __init__(self):
        """Initialize the generator service."""
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        self.llm = LLMService()
        self.tts = TTSService()
        self.file_handler = FileHandler()
    
    def _extract_text_from_sources(self, sources: List[Dict]) -> str:
        """Extract text content from all sources."""
        texts = []
        for source in sources:
            if source.get('type') == 'pdf':
                texts.append(source['text'])
            else:  # Zotero source
                if 'abstractNote' in source['data']:
                    texts.append(source['data']['abstractNote'])
                # TODO: Add support for full-text content from Zotero
        return "\n\n".join(texts)
        
    def _generate_script(self, content: str, title: str, tone: str, duration_minutes: int, language: str) -> Dict:
        """Generate a podcast script from the content."""
        # TODO: Implement LLM-based script generation
        # For now, return a simple template
        return {
            "title": title,
            "summary": f"A {duration_minutes}-minute episode about {title}",
            "script": f"Welcome to this episode about {title}.\n\nHere's what we found in our sources:\n\n{content[:500]}...",
            "language": language,
            "tone": tone
        }
        
    def _generate_audio(self, script: Dict) -> str:
        """Generate audio from the script."""
        # TODO: Implement text-to-speech
        # For now, create a dummy audio file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        temp_file.close()
        return temp_file.name
        
    def generate_episode(
        self,
        sources: List[Dict],
        title: str,
        tone: str = "professional",
        duration_minutes: int = 15,
        language: str = "en"
    ) -> Optional[Dict]:
        """Generate a podcast episode from the given sources."""
        try:
            # Extract content from sources
            content = self._extract_text_from_sources(sources)
            
            # Generate script
            script = self._generate_script(content, title, tone, duration_minutes, language)
            
            # Generate audio
            audio_path = self._generate_audio(script)
            
            # Save transcript
            transcript_path = self.output_dir / f"{title.lower().replace(' ', '_')}_transcript.txt"
            with open(transcript_path, 'w') as f:
                f.write(script['script'])
            
            return {
                "title": script["title"],
                "summary": script["summary"],
                "audio_path": audio_path,
                "transcript_path": str(transcript_path)
            }
        except Exception as e:
            print(f"Error generating episode: {str(e)}")
            return None
    
    def _extract_tags(self, sources: List[Dict]) -> List[str]:
        """Extract unique tags from sources."""
        tags = set()
        for source in sources:
            if source.get('type') == 'pdf':
                # Extract keywords from PDF metadata
                keywords = source.get('metadata', {}).get('keywords', '')
                if keywords:
                    tags.update(keywords.split(','))
            else:
                # Handle Zotero and other sources
                tags.update(source.get("tags", []))
        return list(tags)
    
    def _format_source_for_llm(self, source: Dict) -> str:
        """Format a source for LLM input."""
        if source.get('type') == 'pdf':
            return f"""Source:
Title: {source['metadata'].get('title', 'Unknown')}
Author: {source['metadata'].get('author', 'Unknown')}
Content: {source['text'][:2000]}...  # Truncate long PDFs
"""
        else:
            # Handle Zotero sources
            return f"""Source:
Title: {source['data'].get('title', 'Unknown')}
Authors: {', '.join([author.get('firstName', '') + ' ' + author.get('lastName', '') for author in source['data'].get('creators', [])])}
Abstract: {source['data'].get('abstractNote', '')}
""" 
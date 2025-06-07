from typing import List, Dict, Optional
from pathlib import Path
import time
import json
import os
import tempfile

from app.services.gpt_service import LLMService
from app.services.tts_service import TTSService
from app.services.script_generator import ScriptGenerator
from app.services.prompt_manager import PromptManager
from app.services.library_manager import LibraryManager
from app.utils.file_handler import FileHandler

class Generator:
    def __init__(self):
        """Initialize the generator service."""
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        self.llm = LLMService()
        self.tts = TTSService()
        self.script_generator = ScriptGenerator()
        self.prompt_manager = PromptManager()
        self.library_manager = LibraryManager()
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
        
    def _generate_script(self, content: str, title: str, tone: str, arc: str, duration_minutes: int, language: str) -> Dict:
        """Generate a podcast script from the content using the LLM."""
        prompt = self.prompt_manager.build_prompt(arc, tone)
        script_text = self.script_generator.generate(content, prompt)
        summary = self.llm.generate_summary(script_text)
        return {
            "title": title,
            "summary": summary,
            "script": script_text,
            "language": language,
            "tone": tone,
            "arc": arc,
        }
        
    def _generate_audio(self, script: Dict) -> str:
        """Generate audio from the script using TTS."""
        audio_path = self.output_dir / f"{script['title'].lower().replace(' ', '_')}.mp3"
        success = self.tts.generate_audio(script["script"], str(audio_path))
        return str(audio_path) if success else ""
        
    def generate_episode(
        self,
        sources: List[Dict],
        title: str,
        tone: str = "professional",
        duration_minutes: int = 15,
        language: str = "en",
        arc: str = "Civic Storyteller"
    ) -> Optional[Dict]:
        """Generate a podcast episode from the given sources."""
        try:
            # Extract content from sources
            content = self._extract_text_from_sources(sources)

            # Generate script
            script = self._generate_script(content, title, tone, arc, duration_minutes, language)
            
            # Generate audio
            audio_path = self._generate_audio(script)

            # Save transcript
            transcript_path = self.output_dir / f"{title.lower().replace(' ', '_')}_transcript.txt"
            with open(transcript_path, 'w') as f:
                f.write(script['script'])

            episode_info = {
                "title": script["title"],
                "summary": script["summary"],
                "audio_path": audio_path,
                "transcript_path": str(transcript_path),
                "tags": self._extract_tags(sources),
                "arc": arc,
                "tone": tone,
                "date": time.strftime("%Y-%m-%d"),
            }

            self.library_manager.add_episode(episode_info)

            return episode_info
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
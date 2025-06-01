from typing import List, Dict, Optional
from pathlib import Path
import time

from .gpt_service import LLMService
from .tts_service import TTSService
from ..utils.file_handler import FileHandler

class Generator:
    def __init__(self):
        """Initialize the generator with required services."""
        self.llm = LLMService()
        self.tts = TTSService()
        self.file_handler = FileHandler()
    
    def generate_episode(
        self,
        sources: List[Dict],
        title: str,
        tone: str = "journalistic",
        duration_minutes: int = 15,
        language: str = "en"
    ) -> Optional[Dict]:
        """Generate a complete podcast episode from sources."""
        try:
            # 1. Generate script
            script = self.llm.generate_script(sources, tone, duration_minutes)
            if not script:
                raise Exception("Failed to generate script")
            
            # 2. Generate summary
            summary = self.llm.generate_summary(script)
            if not summary:
                raise Exception("Failed to generate summary")
            
            # 3. Generate audio
            timestamp = int(time.time())
            audio_path = f"output/audio_{timestamp}.mp3"
            success = self.tts.generate_audio(
                text=script,
                output_path=audio_path,
                language=language
            )
            if not success:
                raise Exception("Failed to generate audio")
            
            # 4. Save episode
            tags = self._extract_tags(sources)
            episode_id = self.file_handler.save_episode(
                title=title,
                script=script,
                audio_path=audio_path,
                summary=summary,
                sources=sources,
                tags=tags
            )
            
            if not episode_id:
                raise Exception("Failed to save episode")
            
            return {
                "id": episode_id,
                "title": title,
                "summary": summary,
                "transcript_path": f"output/transcript_{episode_id}.txt",
                "audio_path": audio_path,
                "sources": sources,
                "tags": tags
            }
            
        except Exception as e:
            print(f"Error generating episode: {e}")
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
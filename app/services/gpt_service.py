import ollama
from typing import List, Dict
import os

class LLMService:
    def __init__(self):
        """Initialize Ollama client for Claude."""
        # Ensure Claude model is pulled
        try:
            ollama.pull('claude')
        except Exception as e:
            print(f"Warning: Could not pull Claude model: {e}")
    
    def generate_script(self, sources: List[Dict], tone: str, duration_minutes: int) -> str:
        """Generate a podcast script from the provided sources."""
        # Format each source
        source_texts = []
        for source in sources:
            if source.get('type') == 'pdf':
                source_text = f"""PDF Source:
Title: {source['metadata'].get('title', 'Unknown')}
Author: {source['metadata'].get('author', 'Unknown')}
Content: {source['text'][:2000]}...
"""
            else:
                source_text = f"""Zotero Source:
Title: {source['data'].get('title', 'Untitled')}
Authors: {', '.join([author.get('firstName', '') + ' ' + author.get('lastName', '') for author in source['data'].get('creators', [])])}
Abstract: {source['data'].get('abstractNote', '')}
"""
            source_texts.append(source_text)
        
        sources_text = "\n\n".join(source_texts)
        prompt = (
            "Create an engaging podcast script based on these sources:\n\n"
            f"{sources_text}\n\n"
            "Style guidelines:\n"
            f"- Tone: {tone}\n"
            f"- Target duration: {duration_minutes} minutes\n"
            "- Format: Include introduction, main discussion, and conclusion\n"
            "- Make complex topics accessible while maintaining academic integrity\n"
            "- Use conversational language and clear transitions\n"
            "- Include brief source citations when discussing specific findings\n\n"
            "Please structure the output as a complete podcast script."
        )

        try:
            response = ollama.chat(model='claude', messages=[
                {
                    'role': 'system',
                    'content': 'You are an expert at creating engaging podcast scripts from academic sources.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ])
            return response['message']['content']
        except Exception as e:
            print(f"Error generating script: {e}")
            return ""
    
    def generate_summary(self, script: str) -> str:
        """Generate a brief summary of the podcast script."""
        try:
            response = ollama.chat(model='claude', messages=[
                {
                    'role': 'system',
                    'content': 'Create a brief, engaging summary of this podcast script.'
                },
                {
                    'role': 'user',
                    'content': script
                }
            ])
            return response['message']['content']
        except Exception as e:
            print(f"Error generating summary: {e}")
            return "" 
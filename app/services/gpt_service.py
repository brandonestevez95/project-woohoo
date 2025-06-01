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
        # Prepare the prompt
        source_texts = []
        for i, source in enumerate(sources, 1):
            source_text = f"Source {i}:\n"
            source_text += f"Title: {source['title']}\n"
            source_text += f"Authors: {', '.join(source['authors'])}\n"
            source_text += f"Abstract: {source['abstract']}\n"
            source_texts.append(source_text)
        
        prompt = f"""Create an engaging podcast script based on these academic sources:

{'\n\n'.join(source_texts)}

Style guidelines:
- Tone: {tone}
- Target duration: {duration_minutes} minutes
- Format: Include introduction, main discussion, and conclusion
- Make complex topics accessible while maintaining academic integrity
- Use conversational language and clear transitions
- Include brief source citations when discussing specific findings

Please structure the output as a complete podcast script."""

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
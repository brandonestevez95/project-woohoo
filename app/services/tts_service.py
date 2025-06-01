from gtts import gTTS
from typing import Optional
import os
from pathlib import Path

class TTSService:
    def __init__(self):
        """Initialize TTS service."""
        pass
    
    def generate_audio(
        self,
        text: str,
        output_path: str,
        language: str = "en"
    ) -> bool:
        """Generate audio from text using Google TTS."""
        try:
            # Ensure output directory exists
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Generate audio
            tts = gTTS(text=text, lang=language)
            tts.save(output_path)
            return True
        except Exception as e:
            print(f"Error with TTS: {e}")
            return False
    
    def list_available_languages(self) -> list:
        """List available languages."""
        return [
            "en",  # English
            "es",  # Spanish
            "fr",  # French
            "de",  # German
            "it",  # Italian
            "pt",  # Portuguese
            "ru",  # Russian
            "ja",  # Japanese
            "ko",  # Korean
            "zh",  # Chinese
        ] 
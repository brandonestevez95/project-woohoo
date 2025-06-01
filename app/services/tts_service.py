from TTS.api import TTS
from typing import Optional
import os
from pathlib import Path
import torch

class TTSService:
    def __init__(self):
        """Initialize TTS service."""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # Initialize TTS with a good multi-speaker model
        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(self.device)
    
    def generate_audio(
        self,
        text: str,
        output_path: str,
        voice_preset: str = "v2/en_speaker_6",  # Default to a neutral English voice
        language: str = "en"
    ) -> bool:
        """Generate audio from text using Coqui TTS."""
        try:
            # Ensure output directory exists
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Generate audio
            self.tts.tts_to_file(
                text=text,
                file_path=output_path,
                speaker_wav=None,  # Can be used for voice cloning
                language=language
            )
            return True
        except Exception as e:
            print(f"Error with TTS: {e}")
            return False
    
    def list_available_voices(self) -> list:
        """List available voice presets."""
        # For XTTS v2, these are the available speakers
        return [
            "v2/en_speaker_1",  # Male, enthusiastic
            "v2/en_speaker_2",  # Female, professional
            "v2/en_speaker_3",  # Male, deep
            "v2/en_speaker_4",  # Female, warm
            "v2/en_speaker_5",  # Male, narrative
            "v2/en_speaker_6",  # Female, clear
            "v2/en_speaker_7",  # Male, authoritative
            "v2/en_speaker_8",  # Female, engaging
        ] 
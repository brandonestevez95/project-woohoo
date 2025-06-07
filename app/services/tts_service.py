from typing import Optional
from pathlib import Path

try:
    from TTS.api import TTS
except Exception:
    TTS = None

class TTSService:
    """Text-to-speech service using Coqui XTTS."""

    def __init__(self, model_name: str = "tts_models/multilingual/multi-dataset/xtts_v2"):
        self.model_name = model_name
        self.tts = None
        if TTS:
            try:
                self.tts = TTS(model_name=model_name)
            except Exception as e:
                print(f"Warning initializing TTS model: {e}")

    def generate_audio(self, text: str, output_path: str, voice: Optional[str] = None) -> bool:
        """Generate audio from text using Coqui XTTS."""
        if not self.tts:
            print("TTS model unavailable")
            return False
        try:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            self.tts.tts_to_file(text=text, file_path=output_path, speaker=voice)
            return True
        except Exception as e:
            print(f"Error with TTS: {e}")
            return False

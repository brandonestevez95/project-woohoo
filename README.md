# Project Woohoo 🎙️

An AI-powered tool that transforms academic sources into engaging podcast episodes, using completely free and open-source technologies.

## Features

- 📚 Import sources from Zotero libraries, RSS feeds, or bibliography files
- 🤖 Generate cohesive podcast scripts using Claude (via Ollama)
- 🎧 Convert scripts to high-quality audio using Coqui TTS
- 🌟 Filter, favorite, and manage your episode library
- 📝 Export transcripts and audio files
- 🌐 Everything runs locally - no API keys needed!

## Prerequisites

1. Install [Ollama](https://ollama.ai/) for local LLM support
2. Pull the Claude model:
```bash
ollama pull claude
```

## Setup

1. Clone this repository
2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Unix/Mac
# or
venv\Scripts\activate     # On Windows
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. For better performance on macOS:
```bash
xcode-select --install
pip install watchdog
```

## Usage

Run the Streamlit app:
```bash
streamlit run app/main.py
```

### Available Voices

The TTS system (Coqui XTTS v2) includes 8 high-quality voices:
- Male, enthusiastic (v2/en_speaker_1)
- Female, professional (v2/en_speaker_2)
- Male, deep (v2/en_speaker_3)
- Female, warm (v2/en_speaker_4)
- Male, narrative (v2/en_speaker_5)
- Female, clear (v2/en_speaker_6)
- Male, authoritative (v2/en_speaker_7)
- Female, engaging (v2/en_speaker_8)

### Supported Languages
- English
- Spanish
- French
- German
(More languages available through XTTS v2)

## Project Structure

```
.
├── app/                    # Main application code
│   ├── components/        # UI components
│   ├── services/         # Core services
│   │   ├── gpt_service.py    # LLM integration (Claude)
│   │   ├── tts_service.py    # Text-to-speech (Coqui TTS)
│   │   └── generator.py      # Episode generation pipeline
│   └── utils/           # Helper functions
├── data/                # Input data storage
├── output/             # Generated episodes
└── tests/             # Unit tests
```

## How It Works

1. **Source Import**: Upload academic sources through Zotero, RSS feeds, or bibliography files
2. **Script Generation**: Claude processes the sources into an engaging podcast script
3. **Audio Generation**: Coqui TTS converts the script into natural-sounding audio
4. **Management**: Organize episodes with tags, favorites, and easy export options

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - feel free to use this project for personal or commercial purposes. 
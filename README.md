# Project Woohoo 🎙️

An AI-powered tool that transforms academic sources into engaging podcast episodes, using completely free and open-source technologies.

## Features

- 📚 Import sources from:
  - Zotero libraries
  - PDF documents
  - Bibliography files (.bib, .csv)
- 🤖 Generate cohesive podcast scripts using Claude (via Ollama)
- 🎧 Convert scripts to audio using Google Text-to-Speech (gTTS)
- 🌟 Filter, favorite, and manage your episode library
- 📝 Export transcripts and audio files
- 🌐 Everything runs locally - no API keys needed!
- 📱 Web and desktop versions available

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

### Web Version
Run the Streamlit app:
```bash
streamlit run app/main.py
```

### Desktop Version
Launch the standalone application:
```bash
./dist/ProjectWoohoo/ProjectWoohoo  # On Unix/Mac
# or
dist\ProjectWoohoo\ProjectWoohoo.exe  # On Windows
```

### Supported Languages
- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Italian (it)
- Portuguese (pt)
- Russian (ru)
- Japanese (ja)
- Korean (ko)
- Chinese (zh)

## Project Structure

```
.
├── app/                    # Main application code
│   ├── pages/            # Streamlit pages
│   ├── services/         # Core services
│   │   ├── gpt_service.py    # LLM integration (Claude)
│   │   ├── tts_service.py    # Text-to-speech (gTTS)
│   │   ├── pdf_service.py    # PDF processing
│   │   └── generator.py      # Episode generation pipeline
│   └── utils/           # Helper functions
├── data/                # Input data storage
├── output/             # Generated episodes
└── tests/             # Unit tests
```

## How It Works

1. **Source Import**: Upload academic sources through:
   - Zotero integration
   - PDF document upload
   - Bibliography files
2. **Script Generation**: Claude processes the sources into an engaging podcast script
3. **Audio Generation**: Google TTS converts the script into natural-sounding audio
4. **Management**: Organize episodes with tags, favorites, and easy export options

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - feel free to use this project for personal or commercial purposes. 
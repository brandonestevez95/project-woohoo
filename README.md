# Project Woohoo 🎙️

Transform any text into engaging podcast episodes! Project Woohoo uses AI to convert academic papers, articles, and documents into easy-to-listen podcast content.

## Features

- 🔍 **Smart PDF Processing**: Automatically extracts and structures content from academic papers
- 🎯 **Interest-Based Learning**: Choose from 50+ topics across technology, science, arts, and more
- 🤖 **AI Transformation**: Converts academic text into engaging podcast-style narration
- 🎧 **Audio Generation**: (Coming Soon) High-quality text-to-speech conversion
- 📱 **Interactive Player**: (Coming Soon) Easy-to-use episode player with progress tracking

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/yourusername/operation-woohoo.git
cd operation-woohoo
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python -m streamlit run app/main.py
```

## Project Structure

```
operation-woohoo/
├── app/
│   ├── components/
│   │   ├── __init__.py
│   │   └── onboarding.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── pdf_processor.py
│   │   └── profile_manager.py
│   ├── __init__.py
│   └── main.py
├── data/
│   └── profiles/
├── requirements.txt
└── README.md
```

## Current Features

### PDF Processing
- Automatic section detection
- Text cleaning and normalization
- Academic paper structure recognition
- Preview of content transformation

### User Profiles
- Personalized interest selection
- Progress tracking
- Multi-language support (coming soon)
- Custom voice preferences (coming soon)

### Content Topics
The platform supports learning content across multiple domains:
- Technology & Computing
- Science & Mathematics
- Arts & Humanities
- Design & Architecture
- Business & Economics
- Social Sciences
- Agriculture & Environment
- Health & Medicine

## Development Roadmap

- [ ] Implement AI content transformation
- [ ] Add text-to-speech generation
- [ ] Create interactive episode player
- [ ] Add content recommendation system
- [ ] Implement user progress tracking
- [ ] Add social sharing features

## Contributing

We welcome contributions! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
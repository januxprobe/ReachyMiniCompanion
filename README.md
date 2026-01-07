# Reachy Mini Companion 🤖✨

An AI-powered desk companion built for Reachy Mini robot. Makes your robot a friendly, interactive companion that can see, listen, think, and respond naturally.

## Vision

Create a physical AI companion that:
- **Sees** - Recognizes you and tracks faces
- **Listens** - Understands voice commands and conversations
- **Thinks** - Uses AI/LLM for natural interactions
- **Expresses** - Shows emotions through movements and speech
- **Remembers** - Builds context and personality over time
- **Engages** - Proactive interactions, not just reactive

## Current Status

🚧 **In Development** - Building step by step!

### ✅ Completed
- [x] Project structure setup
- [x] Basic Reachy Mini app framework
- [x] Development environment configured

### 🎯 Next Steps
See [ROADMAP.md](ROADMAP.md) for detailed step-by-step learning plan.

## Project Structure

```
ReachyMiniCompanion/
├── pyproject.toml                  # Python package configuration
├── README.md                       # This file
├── ROADMAP.md                      # Step-by-step development plan
├── reachy_mini_companion/          # Main package
│   ├── __init__.py
│   ├── main.py                     # App entry point
│   └── static/                     # Optional web UI (future)
└── tests/                          # Unit tests (future)
```

## Development Setup

### Prerequisites
- Reachy Mini robot or simulator
- Python 3.10+
- Reachy Mini SDK installed

### Local Development

```bash
# Activate Reachy environment
reachy

# Clone repository
cd ~/Documents/Workspace
git clone https://github.com/januxprobe/ReachyMiniCompanion.git
cd ReachyMiniCompanion

# Install in development mode
pip install -e .

# Test locally (with simulator running)
python reachy_mini_companion/main.py
```

### Testing with Dashboard

```bash
# Install in development mode
pip install -e .

# Start dashboard
reachy-mini-daemon

# Navigate to http://127.0.0.1:8000/
# Install app from local path
# Click Run to test
```

## Installation on Robot

Once published to Hugging Face, users can:
1. Open Reachy Mini dashboard
2. Go to Applications tab
3. Install from Hugging Face Space
4. Click Run

## Learning Approach

This project is built **step by step** with clear learning goals:

1. **Foundation** - Basic app structure ✅
2. **Vision** - Camera and face detection
3. **Interaction** - Emotions and gestures
4. **Intelligence** - AI/LLM integration
5. **Personality** - Memory and context
6. **Polish** - Web UI and refinement

Each step builds on the previous, with testing at each stage.

## Technologies

- **Robot Control**: Reachy Mini SDK
- **Computer Vision**: OpenCV, face detection
- **AI/LLM**: Hugging Face Inference API (planned)
- **Speech**: Text-to-speech synthesis
- **Framework**: ReachyMiniApp (runs via dashboard)

## Contributing

This is a personal learning project, but ideas and suggestions welcome!

## License

Apache 2.0

## About

Built with ❤️ for Reachy Mini

Last updated: January 7, 2026

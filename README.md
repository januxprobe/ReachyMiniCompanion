---
title: Reachy Mini Companion
emoji: 🤖
colorFrom: purple
colorTo: blue
sdk: static
pinned: false
short_description: AI-powered desk companion with emotions, conversations, and personality
tags:
  - reachy_mini
  - reachy_mini_python_app
---

# Reachy Mini Companion 🤖✨

An AI-powered desk companion built for Reachy Mini robot. Have natural voice conversations, get help with daily tasks, and enjoy a companion with personality!

## Vision: The Complete Desk Companion

**Reachy Mini will be:**
- 🗣️ A **conversationalist** you can talk to naturally (voice + text)
- 👀 A **visual assistant** that sees and understands your environment
- 📅 A **proactive helper** for daily planning and wellness
- 🎮 A **gaming buddy** that hypes you up and provides strategy
- 🌍 A **translator** for multilingual conversations
- 🧠 A **creative partner** for brainstorming and problem-solving
- ❤️ A **companion** with personality that feels alive

## Current Status

🚀 **Actively Developing** - Reachy is now a talking, seeing companion!

### ✅ Phase 1: Foundation (Complete!)
- [x] Project structure and development workflow
- [x] Emotion system (4 emotions: happy, sad, excited, curious)
- [x] Antenna behaviors (wave, bounce, droop)
- [x] Movement Manager (non-blocking queue-based execution)

### ✅ Phase 2: Conversation System (Complete!)
- [x] Gemini Live API integration
- [x] Real-time bidirectional voice conversations
- [x] Audio format conversion (stereo/mono, multiple sample rates)
- [x] Back-and-forth natural dialogue
- [x] Integration into main app with auto-start
- [x] Initial greeting (Reachy introduces itself on startup)

### 🔄 Phase 3: Vision & Awareness (In Progress)
- [x] Camera integration with background worker
- [ ] Face detection
- [ ] Head tracking (look at faces)
- [ ] Person recognition

### 🎯 Coming Next
- Face detection and tracking
- Context-aware emotions during conversation
- Proactive life assistant features
- Memory and personality system

See [ROADMAP.md](ROADMAP.md) for detailed development plan.

## Features

### 🎭 Emotions & Expression
Rich emotional expressions using head and antenna movements:
- **Happy** - Looking up with raised antennas
- **Sad** - Looking down with droopy antennas
- **Excited** - Fast nodding with alternating antennas
- **Curious** - Head tilting side to side

### 💬 Real-time Voice Conversations
Natural conversations powered by Google Gemini Live API:
- **Auto-start with greeting** - Reachy introduces itself on startup
- **Bidirectional audio** - You talk → robot responds naturally
- **Continuous dialogue** - Back-and-forth conversation flow
- **Interruption support** - Can interrupt the robot mid-response
- **Clear audio** - Correct playback speed with format conversion

### 👁️ Vision System
Background camera capture for visual awareness:
- **Continuous capture** - Background thread capturing at ~23 FPS
- **Thread-safe access** - Latest frame always available
- **FPS tracking** - Real-time performance monitoring
- **Ready for vision** - Foundation for face detection and tracking

### 🏗️ Architecture
- **Queue-based movement system** - Non-blocking execution with priorities
- **Async audio streaming** - Separate tasks for listen, send, receive, play
- **Background camera worker** - Thread-safe frame capture
- **Format conversion** - Handles stereo/mono, 16kHz/24kHz/48kHz
- **Clean lifecycle management** - Graceful start/stop for all components

## Project Structure

```
ReachyMiniCompanion/
├── reachy_mini_companion/          # Main package
│   ├── main.py                     # ReachyMiniApp entry point
│   ├── emotions.py                 # Emotion system
│   ├── movement_manager.py         # Queue-based movement execution
│   ├── conversation_manager.py     # Gemini Live API integration
│   ├── camera_worker.py            # Background camera capture
│   ├── audio_converters.py         # Audio format conversion
│   └── config.py                   # Configuration management
├── docs/                           # Documentation
│   ├── CONVERSATION_MANAGER.md     # Conversation system API docs
│   └── TESTING.md                  # Testing guide
├── examples/                       # Example scripts (demo_*.py)
│   ├── demo_conversation_integration.py  # Conversation integration demo
│   └── demo_camera_worker.py       # Camera capture demo
├── tests/                          # Test suite (automated tests)
│   ├── test_audio_converters.py    # Audio conversion tests
│   ├── test_gemini_live.py         # Gemini API tests
│   └── test-dashboard.sh           # Automated dashboard test
├── README.md                       # This file
├── ROADMAP.md                      # Development roadmap
├── SESSION_NOTES.md                # Development journal
└── pyproject.toml                  # Package configuration
```

## Quick Start

### Prerequisites
- Reachy Mini robot or simulator
- Python 3.10+
- Reachy Mini SDK installed
- Google Gemini API key

### Installation

```bash
# Clone repository
git clone https://github.com/januxprobe/ReachyMiniCompanion.git
cd ReachyMiniCompanion

# Install in development mode
pip install -e .

# Set up API key
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### Test Voice Conversations

```bash
# Test real-time conversations (30 seconds)
python tests/test_conversation.py --duration 30

# The test will show "🎤 SPEAK NOW!" when ready
# Speak naturally, the robot will respond!
```

### Run via Dashboard

```bash
# Install the app
pip install -e .

# Start Reachy Mini dashboard
mjpython -m reachy_mini.daemon.app.main --sim

# Navigate to http://127.0.0.1:8000/
# Go to Applications tab
# Install from local path
# Click Run
```

## Development

### Testing

```bash
# Quick automated test
./tests/test-dashboard.sh

# Test conversations
python tests/test_conversation.py

# Test audio I/O
python tests/test_audio_echo.py

# Manual validation
reachy-mini-app-assistant check
```

### Project Commands

```bash
# Reinstall after code changes
pip install -e .

# Git workflow
git status
git add .
git commit -m "Description"
git push
```

## Technologies

- **Robot Control**: Reachy Mini SDK
- **AI Conversations**: Google Gemini Live API (native audio)
- **Audio Processing**: NumPy, SciPy (resampling)
- **Async Operations**: asyncio, TaskGroups
- **Computer Vision**: OpenCV (planned)
- **Framework**: ReachyMiniApp (dashboard integration)

## Documentation

- **[ROADMAP.md](ROADMAP.md)** - Complete development plan with phases
- **[SESSION_NOTES.md](SESSION_NOTES.md)** - Development journal and quick reference
- **[docs/TESTING.md](docs/TESTING.md)** - Testing workflow and commands
- **[docs/CONVERSATION_MANAGER.md](docs/CONVERSATION_MANAGER.md)** - Conversation API reference

## Contributing

This is a personal learning project, but ideas and suggestions are welcome! Feel free to open issues or discussions.

## License

Apache 2.0

## About

Building a true AI desk companion, step by step, with learning and experimentation at every stage.

Built with ❤️ for Reachy Mini

---

**Last updated:** January 8, 2026
**Current Phase:** Integrating conversation system into main app
**Repository:** https://github.com/januxprobe/ReachyMiniCompanion

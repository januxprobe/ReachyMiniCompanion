# Reachy Mini Companion - Development Roadmap

Step-by-step learning path to build a complete AI desk companion.

## Philosophy

**Learn by building.** Each step is:
- Self-contained and testable
- Builds on previous steps
- Has clear success criteria
- Teaches specific concepts

---

## Phase 1: Foundation ✅

### Step 1.1: Project Setup ✅
**Goal**: Proper project structure and development environment

**What we learned:**
- Reachy Mini app structure (inheriting from ReachyMiniApp)
- Threading model (background thread with stop_event)
- Package configuration (pyproject.toml)
- Development workflow

**Deliverables:**
- [x] Project structure created
- [x] Basic app template with idle behavior
- [x] Development environment configured
- [x] Can run locally for testing

**Status**: ✅ COMPLETE

### Step 1.2: Emotion System ✅
**Goal**: Rich emotional expressions

**What we learned:**
- Antenna control patterns
- Head movement coordination
- Emotion state management

**Deliverables:**
- [x] 4 core emotions (happy, sad, excited, curious)
- [x] 3 antenna behaviors (wave, bounce, droop)
- [x] EmotionManager class with clean API

**Status**: ✅ COMPLETE

### Step 1.3: Movement Manager ✅
**Goal**: Non-blocking movement execution

**What we learned:**
- Threading with priority queues
- Worker thread pattern
- Graceful shutdown

**Deliverables:**
- [x] Queue-based movement system
- [x] Priority levels (HIGH, NORMAL, LOW)
- [x] Background execution thread
- [x] Non-blocking startup

**Status**: ✅ COMPLETE

---

## Phase 2: Conversation System ✅

### Step 2.1: Gemini API Setup ✅
**Goal**: Connect to Google Gemini Live API

**What we learned:**
- Gemini Live API authentication
- WebSocket-based streaming
- Audio format requirements

**Deliverables:**
- [x] API key configuration
- [x] Test connection script
- [x] Audio format converters

**Status**: ✅ COMPLETE

### Step 2.2: Real-time Voice Conversations ✅
**Goal**: Bidirectional audio streaming with Gemini

**What we learned:**
- Queue-based async architecture
- Sample rate conversion (16kHz/24kHz/48kHz)
- Official Google example pattern
- TaskGroup for concurrent operations

**Deliverables:**
- [x] ConversationManager with queue architecture
- [x] Audio format converters (stereo/mono, resampling)
- [x] Bidirectional streaming (mic ↔ Gemini ↔ speakers)
- [x] Back-and-forth conversations working
- [x] Interruption handling

**Status**: ✅ COMPLETE

### Step 2.3: Integrate into Main App (Next!)
**Goal**: Make it a real desk companion

**What to learn:**
- Integrating ConversationManager into ReachyMiniApp
- Dashboard UI controls for conversations
- Linking emotions to conversation state
- Managing conversation lifecycle

**Tasks:**
- [ ] Add ConversationManager to main.py
- [ ] Create dashboard controls (start/stop conversation)
- [ ] Link emotions to conversation (curious while listening, happy while talking)
- [ ] Add conversation state management
- [ ] Test full companion experience

**Success criteria:**
- Can start conversations from dashboard
- Robot shows appropriate emotions during conversation
- Graceful start/stop of conversations
- Works as integrated desk companion

---

## Phase 3: Vision & Awareness

### Step 3.1: Camera Integration
**Goal**: Access robot camera and display frames

**What to learn:**
- Using robot.media.get_frame()
- Frame processing basics
- Camera vs simulator differences

**Tasks:**
- [ ] Add camera frame capture to app
- [ ] Display FPS and frame stats
- [ ] Test with simulator camera
- [ ] Handle errors gracefully

**Success criteria:**
- Can capture frames from robot camera
- Maintains good FPS (20+)
- Works in headless mode

---

### Step 3.2: Face Detection
**Goal**: Detect faces in camera view

**What to learn:**
- OpenCV face detection
- Haar Cascades
- Detection parameters tuning

**Tasks:**
- [ ] Load face detector
- [ ] Detect faces in frames
- [ ] Track largest face
- [ ] Log detection events

**Success criteria:**
- Reliably detects faces
- Handles no-face scenarios
- Low false positive rate

---

### Step 3.3: Head Tracking
**Goal**: Robot looks at detected faces

**What to learn:**
- Converting pixel coords to robot angles
- Smooth head movement
- Tracking threshold

**Tasks:**
- [ ] Calculate target yaw from face position
- [ ] Move head to track face
- [ ] Add smoothing/threshold
- [ ] Test tracking responsiveness

**Success criteria:**
- Robot tracks face smoothly
- No jittering or over-correction
- Returns to neutral when no face

---

## Phase 4: Enhanced Expression

### Step 4.1: Emotion States
**Goal**: Robot shows emotions based on context

**What to learn:**
- State machine design
- Emotion triggers
- Cooldown management

**Tasks:**
- [ ] Define emotion states (NEUTRAL, CURIOUS, HAPPY, SAD)
- [ ] Implement state machine
- [ ] Add transition triggers
- [ ] Test state flow

**Success criteria:**
- Emotions trigger appropriately
- No rapid switching
- Clean state transitions

---

### Step 4.2: Context-Aware Emotions
**Goal**: Robot emotions respond to conversation

**What to learn:**
- State machine design
- Emotion triggers from conversation
- Smooth transitions

**Tasks:**
- [ ] Link conversation state to emotions
- [ ] Curious when listening
- [ ] Happy when engaged
- [ ] Implement smooth transitions
- [ ] Test emotion flow

**Success criteria:**
- Emotions match conversation context
- No rapid switching
- Natural feeling interactions

---

## Phase 5: Advanced Intelligence

### Step 5.1: Multimodal Conversations (Vision + Voice)
**Goal**: Combine camera vision with conversations

**What to learn:**
- Gemini vision API
- Combining vision + conversation
- Context sharing between modalities

**Tasks:**
- [ ] Capture frames from camera
- [ ] Send frames to Gemini during conversations
- [ ] Enable visual questions ("What is this?", "Read this text")
- [ ] Creative brainstorming with visual aids
- [ ] Document analysis (show documents to robot)

**Use cases:**
- **Creative brainstorming**: Show sketches, get feedback
- **Document analysis**: Show papers, get summaries
- **Visual assistance**: "What should I wear?", "Is this fresh?"

**Success criteria:**
- Can answer questions about what it sees
- Maintains conversation context
- Smooth multimodal integration

---

### Step 5.2: Real-time Translation
**Goal**: Multi-language translation in conversations

**What to learn:**
- Gemini translation capabilities
- Language detection
- Maintaining conversation flow across languages

**Tasks:**
- [ ] Add language selection/detection
- [ ] Enable real-time translation mode
- [ ] Translate both ways (user ↔ Gemini)
- [ ] Support common languages

**Use cases:**
- **Language learning**: Practice conversations
- **Translation assistant**: Translate text shown to camera
- **Multilingual communication**: Talk in one language, hear another

**Success criteria:**
- Accurate real-time translation
- Natural conversation flow
- Multiple languages supported

---

## Phase 6: Memory & Personality

### Step 6.1: Short-term Memory
**Goal**: Remember current conversation

**What to learn:**
- Context window management
- Relevant info extraction
- Memory limitations

**Tasks:**
- [ ] Store recent interactions
- [ ] Retrieve relevant context
- [ ] Limit memory size
- [ ] Clear on restart

**Success criteria:**
- Remembers recent topics
- Refers back appropriately
- Doesn't overflow memory

---

### Step 6.2: Long-term Memory (Advanced)
**Goal**: Remember across sessions

**What to learn:**
- Persistent storage
- Face recognition (revisit)
- User profiles

**Tasks:**
- [ ] Store user preferences
- [ ] Save conversation summaries
- [ ] Load on startup
- [ ] Associate with faces

**Success criteria:**
- Remembers previous sessions
- Personalizes to user
- Persistent across restarts

---

### Step 6.3: Proactive Life Assistant
**Goal**: Daily planning and wellness coaching

**What to learn:**
- Calendar integration (via Gemini)
- Time-based reminders
- Habit tracking through conversation
- Proactive suggestions

**Tasks:**
- [ ] Daily planner features
  - [ ] Proactive calendar management
  - [ ] Morning briefings ("Here's your day...")
  - [ ] Outfit suggestions (with camera)
  - [ ] Meal planning suggestions
- [ ] Wellness & routine coach
  - [ ] Habit tracking through check-ins
  - [ ] Mood tracking
  - [ ] Personalized motivation
  - [ ] Self-care reminders
- [ ] Proactive behaviors
  - [ ] Initiate conversations based on time
  - [ ] Check-in reminders
  - [ ] Celebration of achievements

**Use cases:**
- **Morning routine**: "Good morning! Here's your schedule, weather is nice, and I suggest the blue shirt"
- **Wellness check**: "You mentioned wanting to meditate daily. Have you had time today?"
- **Meal planning**: "It's 6pm, what are you thinking for dinner? I can suggest recipes"

**Success criteria:**
- Helpful without being annoying
- Remembers user preferences
- Adapts to routines
- Feels like a supportive companion

---

### Step 6.4: Gaming & Entertainment Companion
**Goal**: Real-time gaming support and encouragement

**What to learn:**
- Screen capture/vision of gameplay
- Context awareness of game state
- Supportive personality modes

**Tasks:**
- [ ] Real-time strategy advisor
  - [ ] Watch gameplay via camera
  - [ ] Provide tactical suggestions
  - [ ] Identify patterns/vulnerabilities
- [ ] AI quest companion
  - [ ] Access game wikis/databases
  - [ ] Provide lore and stats on demand
  - [ ] Quick info lookup without pausing
- [ ] Gaming wingman
  - [ ] Celebrate wins with excitement
  - [ ] Encourage after losses
  - [ ] Provide real-time hype
  - [ ] Track gaming sessions

**Use cases:**
- **Strategy games**: "Enemy flanking from left, watch your resources"
- **RPGs**: "That boss is weak to fire damage, use your fire spell"
- **General gaming**: "Nice combo! You're getting good at this"

**Success criteria:**
- Helpful without being distracting
- Appropriate emotional responses
- Quick information retrieval
- Feels like a true gaming buddy

---

### Step 6.5: Personality & Core Behaviors
**Goal**: Robot has character and initiative

**What to learn:**
- Personality parameters
- Idle behaviors
- Natural engagement patterns

**Tasks:**
- [ ] Define personality traits
- [ ] Add idle behaviors (looking around, small movements)
- [ ] React to environment
- [ ] Consistent character across all modes

**Success criteria:**
- Consistent personality across all features
- Natural idle behaviors
- Feels alive and present

---

## Phase 7: Polish & Publishing

### Step 7.1: Web Chatbot Interface
**Goal**: Browser-based chat interface for text conversations

**What to learn:**
- FastAPI web serving
- WebSocket for real-time chat
- HTML/JS/CSS for chat UI
- Text-based conversation mode

**Tasks:**
- [ ] Create web chat interface
  - [ ] Chat UI with message history
  - [ ] Real-time message updates
  - [ ] Voice input option (browser speech API)
  - [ ] Image upload for visual questions
- [ ] Settings panel
  - [ ] Conversation mode selection
  - [ ] Personality adjustment
  - [ ] Feature toggles
- [ ] Status dashboard
  - [ ] Robot state
  - [ ] Conversation history
  - [ ] Analytics

**Use cases:**
- **Text conversations**: Type to Reachy when you can't speak
- **Remote access**: Chat from anywhere on your network
- **Document sharing**: Upload images/documents for analysis
- **Quiet mode**: Interact without disturbing others

**Success criteria:**
- Accessible via browser
- Responsive chat interface
- Can switch between voice and text modes
- Shows robot emotions/status
- Maintains conversation context across modalities

---

### Step 7.2: Error Handling & Robustness
**Goal**: Production-ready reliability

**What to learn:**
- Error recovery
- Logging
- Graceful degradation

**Tasks:**
- [ ] Add comprehensive error handling
- [ ] Implement logging
- [ ] Test edge cases
- [ ] Add fallbacks

**Success criteria:**
- Doesn't crash on errors
- Recovers gracefully
- Good error messages

---

### Step 7.3: Documentation & Publishing
**Goal**: Share with community

**What to learn:**
- Documentation best practices
- HF Space publishing
- User onboarding

**Tasks:**
- [ ] Write comprehensive README
- [ ] Add code comments
- [ ] Create demo video
- [ ] Publish to Hugging Face

**Success criteria:**
- Clear documentation
- Easy to install
- Community can use it

---

## Success Metrics

**Technical:**
- Runs stably for hours
- Good performance (20+ FPS detection)
- Fast response times (<2s for AI)
- Clean shutdown on stop

**User Experience:**
- Feels responsive and alive
- Natural interactions
- Appropriate emotions
- Engaging personality

**Learning:**
- Understand each component
- Can modify and extend
- Know trade-offs
- Can debug issues

---

## Current Progress

- [x] Phase 1: Foundation (Complete!)
  - [x] Step 1.1: Project Setup
  - [x] Step 1.2: Emotion System
  - [x] Step 1.3: Movement Manager
- [x] Phase 2: Conversation System (95% Complete!)
  - [x] Step 2.1: Gemini API Setup
  - [x] Step 2.2: Real-time Voice Conversations
  - [ ] **Step 2.3: Integrate into Main App (NEXT!)**
- [ ] Phase 3: Vision & Awareness
  - Camera integration, face detection, head tracking
- [ ] Phase 4: Enhanced Expression
  - Context-aware emotions tied to conversation
- [ ] Phase 5: Advanced Intelligence
  - Multimodal conversations (vision + voice)
  - Real-time translation
- [ ] Phase 6: Memory & Personality
  - Short/long-term memory
  - Proactive life assistant (daily planning, wellness)
  - Gaming companion
  - Core personality behaviors
- [ ] Phase 7: Polish & Publishing
  - Web chatbot interface
  - Error handling & robustness
  - Documentation & publishing

---

## Vision: The Complete Desk Companion

**Reachy Mini will be:**
- 🗣️ A **conversationalist** you can talk to naturally (voice + text)
- 👀 A **visual assistant** that sees and understands your environment
- 📅 A **proactive helper** for daily planning and wellness
- 🎮 A **gaming buddy** that hypes you up and provides strategy
- 🌍 A **translator** for multilingual conversations
- 🧠 A **creative partner** for brainstorming and problem-solving
- ❤️ A **companion** with personality that feels alive

---

*Last updated: January 8, 2026*
*Current focus: Integrate conversation system into main app to create real desk companion*
*Next: Make Reachy a true companion, then add vision, then intelligence features*

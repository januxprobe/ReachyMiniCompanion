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

### Step 5.1: Visual Understanding (Optional)
**Goal**: Show robot things and ask questions

**What to learn:**
- Gemini vision API
- Combining vision + conversation
- Context sharing

**Tasks:**
- [ ] Capture frames from camera
- [ ] Send frames to Gemini
- [ ] Ask visual questions
- [ ] Get multimodal responses

**Success criteria:**
- Can answer questions about what it sees
- Maintains conversation context
- Smooth integration

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

### Step 6.3: Personality & Proactivity
**Goal**: Robot has character and initiative

**What to learn:**
- Personality parameters
- Proactive triggers
- Engagement patterns

**Tasks:**
- [ ] Define personality traits
- [ ] Add idle behaviors
- [ ] Initiate conversations
- [ ] React to environment

**Success criteria:**
- Consistent personality
- Proactive without annoying
- Feels alive

---

## Phase 7: Polish & Publishing

### Step 7.1: Web UI (Optional)
**Goal**: Control panel for settings

**What to learn:**
- FastAPI web serving
- HTML/JS/CSS basics
- Real-time updates

**Tasks:**
- [ ] Create static/ directory
- [ ] Build settings page
- [ ] Add controls
- [ ] Connect to app logic

**Success criteria:**
- Accessible via dashboard ⚙️
- Can adjust settings
- Shows app status

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
- [x] Phase 2: Conversation System (Complete!)
  - [x] Step 2.1: Gemini API Setup
  - [x] Step 2.2: Real-time Voice Conversations
  - [ ] Step 2.3: Integrate into Main App (NEXT!)
- [ ] Phase 3: Vision & Awareness
- [ ] Phase 4: Enhanced Expression
- [ ] Phase 5: Advanced Intelligence
- [ ] Phase 6: Memory & Personality
- [ ] Phase 7: Polish & Publishing

---

*Last updated: January 8, 2026*
*Current focus: Integrate conversation system into main app to create real desk companion*

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

---

## Phase 2: Vision (Next!)

### Step 2.1: Camera Integration
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

### Step 2.2: Face Detection
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

### Step 2.3: Head Tracking
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

## Phase 3: Emotion & Expression

### Step 3.1: Emotion States
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

### Step 3.2: Expressive Gestures
**Goal**: Rich antenna and head movements

**What to learn:**
- Antenna control patterns
- Combining head + antenna
- Movement sequencing

**Tasks:**
- [ ] Create antenna gesture library
- [ ] Curious wave
- [ ] Happy bounce
- [ ] Sad droop
- [ ] Integrate with emotions

**Success criteria:**
- Gestures feel natural
- Complete sequences
- Consistent timing

---

### Step 3.3: Speech Output
**Goal**: Robot speaks phrases

**What to learn:**
- Text-to-speech integration
- Audio playback
- Speech timing

**Tasks:**
- [ ] Set up TTS system
- [ ] Generate speech files
- [ ] Play via robot.media
- [ ] Synchronize with gestures

**Success criteria:**
- Clear speech output
- Good timing with emotions
- Phrases match context

---

## Phase 4: Intelligence

### Step 4.1: AI/LLM Integration
**Goal**: Connect to Hugging Face Inference API

**What to learn:**
- API authentication
- Request/response handling
- Context management

**Tasks:**
- [ ] Set up HF API access
- [ ] Test simple queries
- [ ] Add error handling
- [ ] Implement retry logic

**Success criteria:**
- Can query LLM successfully
- Handles API errors
- Reasonable response time

---

### Step 4.2: Conversation System
**Goal**: Natural back-and-forth conversations

**What to learn:**
- Conversation context
- Turn-taking
- Response generation

**Tasks:**
- [ ] Design conversation flow
- [ ] Maintain context history
- [ ] Generate contextual responses
- [ ] Add personality traits

**Success criteria:**
- Coherent multi-turn conversations
- Context-aware responses
- Consistent personality

---

### Step 4.3: Voice Input (Optional)
**Goal**: Listen to voice commands

**What to learn:**
- Speech recognition
- Intent detection
- Command parsing

**Tasks:**
- [ ] Integrate speech recognition
- [ ] Define command vocabulary
- [ ] Parse intents
- [ ] Trigger actions

**Success criteria:**
- Recognizes voice commands
- Executes correct actions
- Handles misrecognition

---

## Phase 5: Memory & Personality

### Step 5.1: Short-term Memory
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

### Step 5.2: Long-term Memory (Advanced)
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

### Step 5.3: Personality & Proactivity
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

## Phase 6: Polish & Publishing

### Step 6.1: Web UI (Optional)
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

### Step 6.2: Error Handling & Robustness
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

### Step 6.3: Documentation & Publishing
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

- [x] Phase 1: Foundation
- [ ] Phase 2: Vision (NEXT)
- [ ] Phase 3: Emotion & Expression
- [ ] Phase 4: Intelligence
- [ ] Phase 5: Memory & Personality
- [ ] Phase 6: Polish & Publishing

---

*Last updated: January 7, 2026*
*Current focus: Setting up vision system*

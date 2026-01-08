# Gemini Live API - Learning Guide

## 🎙️ Overview

The Gemini Live API enables **real-time voice conversations** with Gemini AI. It's designed for low-latency, bidirectional audio streaming - perfect for our robot companion!

**Key Features**:
- Native audio understanding (no separate STT/TTS needed)
- Low latency for natural conversations
- Interruption support (user can interrupt the AI mid-response)
- Voice Activity Detection (VAD) built-in
- WebSocket-based streaming

---

## Audio Format Requirements

### Input Audio (What We Send to Gemini)
- **Format**: 16-bit PCM (raw audio)
- **Sample rate**: 16,000 Hz (16kHz)
- **Channels**: **Mono (1 channel)** ⚠️
- **MIME type**: `audio/pcm;rate=16000`

### Output Audio (What Gemini Sends Us)
- **Sample rate**: 24,000 Hz (24kHz)
- **Format**: Raw PCM audio
- **Channels**: Mono (1 channel)

### 🚨 Important Difference!
**Robot audio**: 16kHz **stereo** (2 channels)
**Gemini API**: 16kHz **mono** (1 channel)

We need to convert stereo → mono before sending to Gemini!

```python
# Convert stereo to mono: average the two channels
stereo_audio = np.array([...])  # shape: (samples, 2)
mono_audio = stereo_audio.mean(axis=1)  # shape: (samples,)
```

---

## Python API Usage

### 1. Installation

```bash
pip install google-genai
```

### 2. Connection Setup

```python
from google import genai

# Create client
client = genai.Client(api_key="YOUR_API_KEY")

# Configure session
config = {
    "response_modalities": ["AUDIO"],  # Get voice responses
    "system_instruction": "You are Reachy Mini, a friendly desk companion robot..."
}

# Connect to Live API (async)
async with client.aio.live.connect(
    model="gemini-2.5-flash-native-audio-preview-12-2025",
    config=config
) as session:
    # ... use session here
```

### 3. Sending Audio (Microphone → Gemini)

```python
# Send audio chunks in real-time
audio_chunk = np.array([...])  # Mono audio, 16kHz

# Format as required
audio_message = {
    "data": audio_chunk.tobytes(),  # Convert to raw bytes
    "mime_type": "audio/pcm;rate=16000"
}

# Send to Gemini
await session.send_realtime_input(audio=audio_message)
```

### 4. Receiving Audio (Gemini → Speakers)

```python
# Receive responses asynchronously
async for response in session.receive():
    # Check if response contains audio
    if response.server_content and response.server_content.model_turn:
        for part in response.server_content.model_turn.parts:
            if hasattr(part, 'inline_data'):
                # This is audio data from Gemini (24kHz)
                audio_bytes = part.inline_data.data
                # ... play through speakers
```

---

## Session Limits

- **Audio-only sessions**: 15 minutes max
- **Audio + video sessions**: 2 minutes max
- **Token limit**: 128k tokens for native audio models
- Sessions can be extended by managing context carefully

---

## Voice Activity Detection (VAD)

**Automatic VAD** (default): Gemini detects when user stops speaking
- Natural turn-taking
- User can interrupt AI mid-response
- No manual control needed

**Manual VAD** (optional): You control when turns start/end
- Send `activity_start` / `activity_end` control messages
- More control but more complex

For our use case, **automatic VAD is perfect!**

---

## Interruption Handling

A key feature for natural conversation:

```python
# Gemini sends an 'interrupted' flag when user interrupts
if response.server_content.interrupted:
    # User started speaking while AI was responding
    # Stop playing audio immediately!
    audio.stop_playing()
    # Clear any queued audio chunks
    audio_queue.clear()
```

---

## Integration Flow for Reachy Mini

Here's how we'll connect the robot to Gemini:

```
┌─────────────────────────────────────────────────────────┐
│                     Reachy Mini Robot                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Microphone (16kHz stereo)                              │
│       ↓                                                 │
│  get_audio_sample()                                     │
│       ↓                                                 │
│  Convert stereo → mono                                  │
│       ↓                                                 │
│  Send to Gemini Live API ─────────────────────────┐    │
│                                                    │    │
│                                                    ↓    │
│                            ┌──────────────────────────┐ │
│                            │   Gemini Live API        │ │
│                            │  (WebSocket Session)     │ │
│                            └──────────────────────────┘ │
│                                                    │    │
│  Receive from Gemini ←─────────────────────────────┘    │
│       ↓                                                 │
│  Resample 24kHz → 16kHz (optional)                      │
│       ↓                                                 │
│  Convert mono → stereo                                  │
│       ↓                                                 │
│  push_audio_sample()                                    │
│       ↓                                                 │
│  Speakers (16kHz stereo)                                │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Key Components We Need to Build:

1. **Audio Converter**
   - Stereo → mono for input
   - Mono → stereo for output
   - Optionally resample 24kHz → 16kHz

2. **Input Stream Handler** (Thread 1)
   - Continuously read from `robot.media.audio.get_audio_sample()`
   - Convert to mono
   - Send to Gemini via `session.send_realtime_input()`

3. **Output Stream Handler** (Thread 2)
   - Continuously receive from Gemini
   - Handle interruptions
   - Convert to stereo
   - Send to `robot.media.audio.push_audio_sample()`

4. **Session Manager**
   - Establish WebSocket connection
   - Handle reconnections
   - Manage conversation context
   - Monitor token usage

---

## Example: Basic Conversation Flow

```python
async def run_conversation():
    # 1. Connect to Gemini
    async with client.aio.live.connect(model=MODEL, config=CONFIG) as session:

        # 2. Start robot audio
        robot.media.audio.start_recording()
        robot.media.audio.start_playing()

        # 3. Run two tasks in parallel
        await asyncio.gather(
            input_stream_task(robot, session),   # Mic → Gemini
            output_stream_task(robot, session)   # Gemini → Speakers
        )

async def input_stream_task(robot, session):
    """Send microphone audio to Gemini"""
    while True:
        chunk = robot.media.audio.get_audio_sample()
        if chunk is not None:
            # Convert stereo to mono
            mono = chunk.mean(axis=1)
            # Send to Gemini
            await session.send_realtime_input(
                audio={"data": mono.tobytes(), "mime_type": "audio/pcm;rate=16000"}
            )
        await asyncio.sleep(0.01)

async def output_stream_task(robot, session):
    """Receive audio from Gemini and play it"""
    async for response in session.receive():
        if response.server_content and response.server_content.model_turn:
            for part in response.server_content.model_turn.parts:
                if hasattr(part, 'inline_data'):
                    # Got audio from Gemini
                    audio_bytes = part.inline_data.data
                    # Convert to numpy, resample if needed, convert to stereo
                    # ... then play
                    robot.media.audio.push_audio_sample(stereo_chunk)
```

---

## Audio Format Conversions Needed

### 1. Stereo to Mono (for input)

```python
def stereo_to_mono(stereo_audio: np.ndarray) -> np.ndarray:
    """
    Convert stereo (2 channels) to mono (1 channel).

    Args:
        stereo_audio: shape (samples, 2), dtype float32

    Returns:
        mono_audio: shape (samples,), dtype float32
    """
    return stereo_audio.mean(axis=1)
```

### 2. Mono to Stereo (for output)

```python
def mono_to_stereo(mono_audio: np.ndarray) -> np.ndarray:
    """
    Convert mono (1 channel) to stereo (2 channels).

    Args:
        mono_audio: shape (samples,), dtype float32

    Returns:
        stereo_audio: shape (samples, 2), dtype float32
    """
    return np.column_stack([mono_audio, mono_audio])
```

### 3. Resample 24kHz → 16kHz (optional)

Gemini outputs 24kHz audio, but our robot uses 16kHz. We can either:

**Option A**: Play 24kHz audio directly (may work if soundcard supports it)
**Option B**: Resample to 16kHz using `scipy` or `resampy`

```python
from scipy import signal

def resample_24k_to_16k(audio_24k: np.ndarray) -> np.ndarray:
    """Resample from 24kHz to 16kHz."""
    # 24000 / 16000 = 1.5, so we need 2/3 of the samples
    return signal.resample(audio_24k, len(audio_24k) * 2 // 3)
```

---

## Error Handling

Common issues and solutions:

### Connection Errors
```python
try:
    async with client.aio.live.connect(...) as session:
        # ... use session
except Exception as e:
    print(f"Connection failed: {e}")
    # Retry with exponential backoff
```

### Session Timeout (15 minutes)
```python
# Monitor session duration
start_time = time.time()
if time.time() - start_time > 14 * 60:  # 14 minutes
    print("Session expiring soon, reconnecting...")
    # Close and reconnect
```

### Audio Buffer Overflow
```python
# Use asyncio.Queue with maxsize
audio_queue = asyncio.Queue(maxsize=100)
```

---

## Security Notes

- **Never hardcode API keys** - use environment variables
- **Rate limiting** - Gemini Live API has usage limits
- **Monitor costs** - Each session consumes tokens

---

## Next Steps

Now that we understand both systems:

1. ✅ Robot audio system (16kHz stereo, chunk-based)
2. ✅ Gemini Live API (16kHz mono input, 24kHz mono output)
3. 🔜 Build audio converters (stereo/mono, resampling)
4. 🔜 Build conversation manager (WebSocket handling)
5. 🔜 Test end-to-end conversation

---

## Key Takeaways

✅ Gemini Live API uses WebSocket for real-time streaming
✅ Audio format: 16kHz PCM mono (we have 16kHz stereo)
✅ Need to convert: stereo → mono (input), mono → stereo (output)
✅ Automatic VAD and interruption handling built-in
✅ Two parallel async tasks: input stream + output stream
✅ Session limits: 15 minutes for audio-only

---

## Sources

- [Gemini Live API Overview](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/live-api)
- [Get Started with Live API](https://ai.google.dev/gemini-api/docs/live)
- [Live API Capabilities Guide](https://ai.google.dev/gemini-api/docs/live-guide)
- [How to Use Gemini Live API Native Audio](https://cloud.google.com/blog/topics/developers-practitioners/how-to-use-gemini-live-api-native-audio-in-vertex-ai)

---

*Last updated: January 8, 2026*

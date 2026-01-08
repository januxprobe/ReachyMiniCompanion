# Conversation Manager - User Guide

## 🎤 Overview

The `ConversationManager` enables **real-time voice conversations** between Reachy Mini and Google's Gemini AI. It handles all the complexity of bidirectional audio streaming, format conversion, and session management.

---

## Quick Start

### Basic Usage

```python
import asyncio
from reachy_mini import ReachyMini
from reachy_mini_companion.conversation_manager import ConversationManager
from reachy_mini_companion.config import config

async def main():
    # Create robot instance (audio only)
    robot = ReachyMini(media_backend="default_no_video")

    # Create conversation manager
    manager = ConversationManager(
        robot=robot,
        api_key=config.GEMINI_API_KEY
    )

    # Start conversation
    await manager.start_conversation()

    # Keep running until interrupted
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await manager.stop_conversation()

asyncio.run(main())
```

### Quick Test

Test the conversation system for 30 seconds:

```bash
python tests/test_conversation.py --duration 30
```

---

## Architecture

The ConversationManager runs two concurrent async tasks:

```
┌─────────────────────────────────────────────────────────┐
│                  Conversation Manager                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  INPUT TASK (Mic → Gemini):                             │
│    Robot Microphone (16kHz stereo)                       │
│         ↓                                                │
│    prepare_for_gemini() → 16kHz mono PCM                 │
│         ↓                                                │
│    Gemini Live API (WebSocket)                           │
│                                                          │
│  OUTPUT TASK (Gemini → Speakers):                       │
│    Gemini Live API (24kHz mono PCM)                      │
│         ↓                                                │
│    prepare_from_gemini() → 16kHz stereo                  │
│         ↓                                                │
│    Robot Speakers                                        │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

Both tasks run **simultaneously** for true real-time conversation.

---

## API Reference

### ConversationManager

```python
ConversationManager(
    robot: ReachyMini,
    api_key: str,
    model: str = "gemini-2.0-flash-exp",
    system_instruction: Optional[str] = None,
    verbose: bool = True
)
```

**Parameters**:
- `robot`: ReachyMini instance with audio enabled
- `api_key`: Google Gemini API key
- `model`: Gemini model name (default: "gemini-2.0-flash-exp")
- `system_instruction`: Custom system prompt for Gemini behavior
- `verbose`: Print debug information (default: True)

**Methods**:

#### `await start_conversation()`
Starts the conversation session. This:
1. Connects to Gemini Live API via WebSocket
2. Starts robot audio recording and playback
3. Launches input and output streaming tasks

#### `await stop_conversation()`
Stops the conversation session. This:
1. Cancels streaming tasks gracefully
2. Closes WebSocket connection
3. Stops robot audio
4. Prints session statistics

#### `await run_conversation(duration_seconds: Optional[float] = None)`
Convenience method that starts, waits, and stops the conversation.
- `duration_seconds`: How long to run (None = forever)

---

## Advanced Usage

### Custom System Instruction

Customize Gemini's personality and behavior:

```python
manager = ConversationManager(
    robot=robot,
    api_key=config.GEMINI_API_KEY,
    system_instruction=(
        "You are Reachy Mini, an expert programming assistant. "
        "Help users with code, answer technical questions, "
        "and explain concepts clearly. Keep responses concise."
    )
)
```

### Access Session Statistics

```python
# After stopping conversation
print(f"Input chunks sent: {manager.stats['input_chunks_sent']}")
print(f"Output chunks received: {manager.stats['output_chunks_received']}")
print(f"Interruptions: {manager.stats['interruptions']}")
print(f"Errors: {manager.stats['errors']}")
```

### Timed Conversation

Run a conversation for exactly 60 seconds:

```python
await manager.run_conversation(duration_seconds=60)
```

---

## Features

### ✅ Automatic Format Conversion

The manager automatically handles all audio format conversions:
- **Input**: Robot stereo → Gemini mono
- **Output**: Gemini 24kHz → Robot 16kHz
- **Format**: float32 ↔ 16-bit PCM

### ✅ Interruption Handling

Users can interrupt the AI mid-response:
- Gemini detects when user starts speaking
- Sends `interrupted` flag
- Manager immediately stops playback
- Clears audio queue
- Ready for new input

### ✅ Error Recovery

Handles common errors gracefully:
- WebSocket disconnections
- Audio buffer overflows
- Invalid audio formats
- API rate limits

### ✅ Statistics Tracking

Monitors conversation health:
- Input/output chunk counts
- Data rates (chunks/second)
- Number of interruptions
- Error counts
- Session duration

---

## Examples

### Example 1: Basic Conversation

```python
# examples/simple_conversation.py
import asyncio
from reachy_mini import ReachyMini
from reachy_mini_companion.conversation_manager import ConversationManager
from reachy_mini_companion.config import config

async def main():
    robot = ReachyMini(media_backend="default_no_video")

    manager = ConversationManager(
        robot=robot,
        api_key=config.GEMINI_API_KEY,
        verbose=True
    )

    print("🎙️  Conversation starting...")
    print("Speak to the robot!")

    try:
        await manager.start_conversation()
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await manager.stop_conversation()

asyncio.run(main())
```

### Example 2: Timed Test

```python
# Quick 30-second conversation test
from reachy_mini_companion.conversation_manager import run_conversation_test

asyncio.run(run_conversation_test(duration_seconds=30))
```

### Example 3: Multiple Sessions

```python
async def main():
    robot = ReachyMini(media_backend="default_no_video")
    manager = ConversationManager(robot=robot, api_key=config.GEMINI_API_KEY)

    # Session 1: 30 seconds
    print("Session 1: General conversation")
    manager.system_instruction = "You are a friendly assistant."
    await manager.run_conversation(duration_seconds=30)

    # Session 2: 30 seconds with different personality
    print("Session 2: Technical assistant")
    manager.system_instruction = "You are a technical expert."
    await manager.run_conversation(duration_seconds=30)

asyncio.run(main())
```

---

## Testing

### Test 1: Basic Functionality

```bash
python tests/test_conversation.py --duration 30
```

This tests:
- WebSocket connection
- Audio streaming (both directions)
- Format conversions
- Graceful shutdown

### Test 2: Interruption

During a conversation:
1. Let Gemini start responding
2. Start speaking while Gemini is talking
3. Gemini should stop and listen to you

### Test 3: Long Conversation

```bash
python tests/test_conversation.py --duration 300
```

Tests stability over 5 minutes.

---

## Troubleshooting

### Issue: No audio output

**Check**:
1. Robot speakers are working: `python tests/test_audio_echo.py`
2. API key is valid
3. Model supports audio output: `gemini-2.0-flash-exp`

### Issue: Audio is choppy

**Possible causes**:
- Network latency (Gemini API connection)
- CPU overload
- Audio buffer underrun

**Solutions**:
- Check network connection
- Reduce other running processes
- Increase audio queue size in code

### Issue: "Connection closed" error

**Possible causes**:
- Session timeout (15 minutes for audio-only)
- Network interruption
- Invalid audio format

**Solutions**:
- Implement automatic reconnection
- Check audio format conversion
- Monitor session duration

### Issue: Gemini doesn't respond

**Check**:
1. Microphone is capturing audio: Check `input_chunks_sent` statistic
2. Audio has sufficient amplitude (speak louder)
3. Audio format is correct (16kHz mono PCM)

---

## Performance Tips

### Optimize Latency

1. **Use wired connection** instead of WiFi
2. **Reduce audio chunk size** (10ms → 5ms)
3. **Use faster model** if available
4. **Minimize processing** between audio I/O

### Optimize Quality

1. **Use external microphone** for better input
2. **Adjust system volume** for optimal levels
3. **Reduce background noise**
4. **Position microphone** properly

### Monitor Performance

```python
# Check streaming rates
stats = manager.stats
input_rate = stats['input_chunks_sent'] / duration
output_rate = stats['output_chunks_received'] / duration

print(f"Input: {input_rate:.1f} chunks/sec (target: ~100)")
print(f"Output: {output_rate:.1f} chunks/sec")
```

Target input rate: ~100 chunks/second (10ms intervals)

---

## Architecture Details

### Async/Await Pattern

The manager uses asyncio for concurrent operations:

```python
# Two tasks run simultaneously
self._input_task = asyncio.create_task(self._input_stream_handler())
self._output_task = asyncio.create_task(self._output_stream_handler())

# Both tasks share the same WebSocket session
async for response in self._gemini_session.receive():
    # Process audio chunks...
```

### Audio Format Pipeline

**Input (Mic → Gemini)**:
```
Robot: (samples, 2) float32 -1.0 to 1.0
    ↓ stereo_to_mono()
Mono: (samples,) float32
    ↓ float32_to_pcm16()
PCM: bytes (16-bit little-endian)
    ↓ send_realtime_input()
Gemini Live API
```

**Output (Gemini → Speakers)**:
```
Gemini Live API (24kHz PCM bytes)
    ↓ pcm16_to_float32()
Mono 24kHz: (samples,) float32
    ↓ resample_24k_to_16k()
Mono 16kHz: (samples,) float32
    ↓ mono_to_stereo()
Robot: (samples, 2) float32
    ↓ push_audio_sample()
Speakers
```

### Session Lifecycle

1. **Initialization**: Create ConversationManager instance
2. **Connection**: `start_conversation()` opens WebSocket
3. **Streaming**: Input/output tasks run concurrently
4. **Interruption**: User can interrupt at any time
5. **Completion**: `stop_conversation()` cleans up gracefully

---

## Best Practices

### Do's ✅

- Always call `stop_conversation()` to clean up resources
- Use `media_backend="default_no_video"` to avoid camera conflicts
- Monitor statistics to detect issues
- Handle KeyboardInterrupt for graceful shutdown
- Test with echo test before conversation test

### Don'ts ❌

- Don't start multiple conversations on same robot instance
- Don't modify audio while streaming
- Don't forget to await async methods
- Don't hardcode API keys in code
- Don't skip error handling

---

## Next Steps

Now that you have the conversation manager:

1. **Test it** with `python tests/test_conversation.py`
2. **Customize** the system instruction for your use case
3. **Integrate** into your Reachy Mini application
4. **Build** higher-level features (wake words, multi-turn dialogues)

---

## Key Takeaways

✅ ConversationManager handles all bidirectional streaming
✅ Audio format conversions are automatic
✅ Interruption handling built-in
✅ Statistics tracking for monitoring
✅ Clean async/await API
✅ Production-ready with error handling

---

*Last updated: January 8, 2026*

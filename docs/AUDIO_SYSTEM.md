# Reachy Mini Audio System - Learning Guide

## 🎧 Overview

The Reachy Mini robot has built-in **microphone** and **speaker** capabilities. This document explains how they work and how to use them.

---

## Hardware: ReSpeaker Microphone Array

**What it is**: A USB microphone array with 4 microphones arranged in a circle

**Capabilities**:
- **Multi-channel audio**: 2 channels (stereo)
- **Sample rate**: 16,000 Hz (16kHz) - telephone quality
- **Direction detection**: Can detect where sound is coming from (DoA - Direction of Arrival)
- **Built-in speakers**: Can play audio back

**Why 16kHz?**
- Good balance between quality and data size
- Standard for speech recognition
- Same as phone call quality
- Much smaller than music quality (44.1kHz)

---

## Software API: robot.media.audio

### How to Access

```python
from reachy_mini import ReachyMini

robot = ReachyMini()
audio = robot.media.audio  # This is the audio interface
```

### Recording Audio (Microphone)

**Start recording**:
```python
audio.start_recording()
```

**Get audio data** (continuous loop):
```python
while True:
    audio_chunk = audio.get_audio_sample()
    if audio_chunk is not None:
        # audio_chunk is a numpy array: shape (samples, 2)
        # 2 channels (stereo), 16kHz sample rate
        # dtype: np.float32, values between -1.0 and 1.0
        print(f"Got {len(audio_chunk)} samples")
```

**Stop recording**:
```python
audio.stop_recording()
```

### Playing Audio (Speakers)

**Method 1: Stream audio data** (for realtime)
```python
audio.start_playing()

# Push audio chunks continuously
audio.push_audio_sample(audio_data)  # audio_data: numpy array (samples, 2)

audio.stop_playing()
```

**Method 2: Play a sound file** (simple)
```python
audio.play_sound("/path/to/sound.wav")
```

### Audio Format Details

**Input (from microphone)**:
- Shape: `(num_samples, 2)` - 2D array
- Channels: 2 (left and right)
- Sample rate: 16,000 Hz
- Data type: `np.float32`
- Value range: -1.0 to 1.0 (normalized)

**Output (to speakers)**:
- Same format as input
- Shape: `(num_samples, 2)`
- Must match sample rate: 16,000 Hz

---

## Example: Echo Test

Record audio and play it back:

```python
from reachy_mini import ReachyMini
import time

robot = ReachyMini()
audio = robot.media.audio

# Start recording
audio.start_recording()
print("Recording for 3 seconds...")

# Record chunks
chunks = []
start_time = time.time()
while time.time() - start_time < 3.0:
    chunk = audio.get_audio_sample()
    if chunk is not None:
        chunks.append(chunk)
    time.sleep(0.01)  # 10ms between reads

audio.stop_recording()
print(f"Recorded {len(chunks)} chunks")

# Play back
print("Playing back...")
audio.start_playing()
for chunk in chunks:
    audio.push_audio_sample(chunk)
    time.sleep(0.01)
audio.stop_playing()
print("Done!")
```

---

## Direction Detection (Optional Feature)

Get the direction of sound:

```python
direction, speech_detected = audio.get_DoA()

# direction: angle in radians
#   0 = left
#   π/2 = front/back
#   π = right

# speech_detected: bool (True if speech is detected)
```

**Note**: Requires firmware 2.1.0+ on ReSpeaker device.

---

## Audio Streaming Flow

**For Gemini Live API**, we'll create this flow:

```
Microphone → get_audio_sample() → [encode] → Gemini Live API
                                              ↓
Speaker ← push_audio_sample() ← [decode] ← Gemini Live API
```

Both directions happen **simultaneously** in separate threads!

---

## Important Concepts

### 1. Chunks (not files!)
- Audio is processed in **chunks** (small pieces)
- Each chunk: ~10-100ms of audio
- Allows real-time streaming
- Low latency for conversation

### 2. Sample Rate (16kHz)
- 16,000 samples per second
- Each sample: one moment in time
- 2 channels = 2 samples at same time (left/right)
- 1 second = 16,000 × 2 = 32,000 values

### 3. Normalization (-1.0 to 1.0)
- Audio amplitudes are scaled
- -1.0 = maximum negative (quietest)
- 0.0 = silence
- 1.0 = maximum positive (loudest)
- Easy for algorithms to process

### 4. Numpy Arrays
- Audio data is in numpy arrays
- Efficient for processing
- Shape: `(samples, channels)`
- Example: `(1600, 2)` = 0.1 seconds of stereo audio

---

## Next Steps

Now that you understand the robot's audio capabilities, we'll:

1. **Test the microphone** - Can we capture audio?
2. **Test the speakers** - Can we play audio?
3. **Learn Gemini Live API** - How to stream audio to/from Gemini
4. **Build the bridge** - Connect robot audio ↔ Gemini

---

## Key Takeaways

✅ Robot has 16kHz stereo audio (microphone + speakers)
✅ Audio is streamed in chunks (real-time processing)
✅ Simple API: `get_audio_sample()` and `push_audio_sample()`
✅ Perfect for conversational AI!

---

*Last updated: January 8, 2026*

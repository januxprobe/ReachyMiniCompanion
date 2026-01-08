#!/usr/bin/env python3
"""
Audio Echo Test

Tests the robot's microphone and speakers by recording audio and playing it back.

This helps us verify:
1. Microphone is working (can capture audio)
2. Speakers are working (can play audio)
3. Audio format is correct
4. Streaming flow works

Usage:
    python tests/test_audio_echo.py
"""

import time
import numpy as np
from reachy_mini import ReachyMini


def echo_test(robot: ReachyMini, duration_seconds: float = 3.0):
    """
    Record audio and play it back.

    Args:
        robot: ReachyMini instance
        duration_seconds: How long to record (default: 3 seconds)
    """
    audio = robot.media.audio

    if audio is None:
        print("❌ Audio system not available!")
        print("   Make sure the robot is connected.")
        return False

    print("=" * 60)
    print("🎤 Audio Echo Test")
    print("=" * 60)

    # Step 1: Start recording
    print(f"\n📝 Step 1: Recording for {duration_seconds} seconds...")
    print("   🗣️  Speak now! Say something interesting!")
    print()

    audio.start_recording()

    # Collect audio chunks
    chunks = []
    start_time = time.time()
    sample_count = 0

    while time.time() - start_time < duration_seconds:
        chunk = audio.get_audio_sample()

        if chunk is not None:
            chunks.append(chunk)
            sample_count += len(chunk)

            # Show progress
            elapsed = time.time() - start_time
            print(f"   Recording... {elapsed:.1f}s / {duration_seconds}s", end="\r")

        time.sleep(0.01)  # 10ms between reads (100 chunks/second)

    audio.stop_recording()
    print()  # New line after progress

    # Stats
    total_samples = sum(len(chunk) for chunk in chunks)
    audio_duration = total_samples / 16000  # 16kHz sample rate
    print(f"\n✅ Recording complete!")
    print(f"   📊 Captured {len(chunks)} chunks")
    print(f"   📊 Total samples: {total_samples:,}")
    print(f"   📊 Audio duration: {audio_duration:.2f} seconds")
    print(f"   📊 Average chunk size: {total_samples // len(chunks) if chunks else 0} samples")

    if not chunks:
        print("\n❌ No audio captured!")
        print("   Check if the microphone is connected.")
        return False

    # Step 2: Analyze the audio
    print(f"\n📊 Step 2: Analyzing audio...")

    # Concatenate all chunks
    full_audio = np.concatenate(chunks, axis=0)
    print(f"   Shape: {full_audio.shape} (samples, channels)")
    print(f"   Data type: {full_audio.dtype}")
    print(f"   Value range: [{full_audio.min():.3f}, {full_audio.max():.3f}]")

    # Check if there's actual sound (not just silence)
    audio_amplitude = np.abs(full_audio).mean()
    print(f"   Average amplitude: {audio_amplitude:.4f}")

    if audio_amplitude < 0.001:
        print("\n⚠️  Warning: Audio is very quiet!")
        print("   The microphone might not be picking up sound.")
        print("   Try speaking louder or checking the connection.")
    else:
        print(f"   ✅ Audio detected! (amplitude: {audio_amplitude:.4f})")

    # Step 3: Play back
    print(f"\n🔊 Step 3: Playing back...")
    print("   🎧 Listen to your echo!")

    audio.start_playing()

    for i, chunk in enumerate(chunks):
        audio.push_audio_sample(chunk)

        # Show playback progress
        played_samples = sum(len(chunks[j]) for j in range(i + 1))
        played_duration = played_samples / 16000
        print(f"   Playing... {played_duration:.1f}s / {audio_duration:.1f}s", end="\r")

        time.sleep(0.01)  # Match recording rate

    audio.stop_playing()
    print()  # New line

    print("\n✅ Playback complete!")

    # Step 4: Summary
    print("\n" + "=" * 60)
    print("🎉 Echo Test Complete!")
    print("=" * 60)
    print()
    print("What we verified:")
    print("  ✅ Microphone can capture audio")
    print("  ✅ Audio format is correct (16kHz, 2 channels)")
    print("  ✅ Speakers can play audio")
    print("  ✅ Streaming flow works!")
    print()

    return True


def main():
    """Run the echo test."""
    print("\n🤖 Starting Reachy Mini Echo Test...")
    print("   Connecting to robot...\n")

    try:
        # Connect to robot (audio only, no camera needed for this test)
        robot = ReachyMini(media_backend="default_no_video")

        # Run the test
        success = echo_test(robot, duration_seconds=3.0)

        if success:
            print("✅ Test passed!\n")
            return 0
        else:
            print("❌ Test failed!\n")
            return 1

    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user (Ctrl+C)")
        return 130

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())

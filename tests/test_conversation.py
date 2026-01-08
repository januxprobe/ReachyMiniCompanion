#!/usr/bin/env python3
"""
Conversation Manager Test

Tests the full bidirectional audio streaming between Reachy Mini and Gemini.

This is an integration test that requires:
1. A valid Gemini API key
2. Robot or simulator running
3. Microphone and speakers working

Usage:
    python tests/test_conversation.py [--duration SECONDS]
"""

import asyncio
import argparse
from reachy_mini_companion.conversation_manager import run_conversation_test


def main():
    """Run the conversation test."""
    parser = argparse.ArgumentParser(
        description="Test conversation between Reachy Mini and Gemini"
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=30.0,
        help="Conversation duration in seconds (default: 30)",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Reduce verbosity",
    )

    args = parser.parse_args()

    print("\n" + "=" * 60)
    print("🎤 Reachy Mini ↔ Gemini Conversation Test")
    print("=" * 60)
    print()
    print("Instructions:")
    print("1. Make sure your robot/simulator is running")
    print("2. Make sure your microphone and speakers are working")
    print("3. Speak naturally to the robot")
    print("4. The robot will respond with voice")
    print("5. You can interrupt the robot at any time")
    print()
    print(f"Test will run for {args.duration} seconds")
    print("Press Ctrl+C to stop early")
    print("=" * 60 + "\n")

    async def run_with_countdown():
        """Run the test with a countdown."""
        # Give user time to prepare
        print("⏰ Starting in 3 seconds...")
        await asyncio.sleep(1)
        print("⏰ 2...")
        await asyncio.sleep(1)
        print("⏰ 1...")
        await asyncio.sleep(1)
        print("\n" + "🎤" * 20)
        print("🎤 SPEAK NOW! Say something to the robot...")
        print("🎤" * 20 + "\n")

        await run_conversation_test(
            duration_seconds=args.duration,
            verbose=not args.quiet,
        )

    try:
        asyncio.run(run_with_countdown())
        return 0
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

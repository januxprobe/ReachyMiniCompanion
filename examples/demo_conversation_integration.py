#!/usr/bin/env python3
"""
Demo: Conversation Integration

Demonstrates the conversation system integrated into ReachyMiniCompanion main app.

This demonstrates:
- Starting a conversation from the main app
- Stopping a conversation gracefully
- Emotion integration (curious emotion when starting)

Usage:
    python examples/demo_conversation_integration.py
"""

import time
from reachy_mini import ReachyMini
from reachy_mini_companion.main import ReachyMiniCompanion


def main():
    """Test conversation integration in main app."""
    print("\n" + "=" * 60)
    print("🤖 Testing Conversation Integration")
    print("=" * 60)

    # Create robot instance
    print("\nConnecting to robot...")
    robot = ReachyMini(media_backend="default_no_video")

    # Create companion app
    print("Initializing companion app...")
    app = ReachyMiniCompanion()
    app.initialize_companion(robot)

    print("\n" + "=" * 60)
    print("✅ Companion Ready!")
    print("=" * 60)

    try:
        # Start conversation
        print("\nStarting conversation in 2 seconds...")
        print("(You should see the curious emotion)")
        time.sleep(2)

        app.start_conversation()

        # Let conversation run for a bit
        print("\nConversation running...")
        print("Speak to the robot! It will listen and respond.")
        print("\nPress Ctrl+C to stop the conversation.\n")

        # Keep running until interrupted
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n\nStopping...")
    finally:
        # Stop conversation
        app.stop_conversation()

        # Cleanup
        app.cleanup(robot)

    print("\n" + "=" * 60)
    print("✅ Test Complete")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()

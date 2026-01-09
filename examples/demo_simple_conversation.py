#!/usr/bin/env python3
"""
Demo: Simple Conversation

A minimal example showing how to use the ConversationManager
to enable voice conversations with Reachy Mini.

This demonstrates:
- Basic conversation setup
- Bidirectional audio streaming
- Graceful shutdown

Usage:
    python examples/demo_simple_conversation.py
"""

import asyncio
from reachy_mini import ReachyMini
from reachy_mini_companion.conversation_manager import ConversationManager
from reachy_mini_companion.config import config


async def main():
    """Run a simple conversation."""
    print("\n" + "=" * 60)
    print("🤖 Reachy Mini - Simple Conversation Example")
    print("=" * 60)
    print("\nSetting up conversation...")

    # 1. Create robot instance (audio only)
    print("   Connecting to robot...")
    robot = ReachyMini(media_backend="default_no_video")

    # 2. Create conversation manager
    print("   Creating conversation manager...")
    manager = ConversationManager(
        robot=robot,
        api_key=config.GEMINI_API_KEY,
        system_instruction=(
            "You are Reachy Mini, a helpful desk companion robot. "
            "Keep your responses brief and friendly."
        ),
        verbose=True,
    )

    # 3. Start conversation
    print("\n" + "=" * 60)
    print("🎙️  Conversation Active!")
    print("=" * 60)
    print("\nSpeak to the robot to start a conversation.")
    print("The robot will listen and respond with voice.")
    print("\nPress Ctrl+C to stop.\n")

    try:
        await manager.start_conversation()

        # Keep running until interrupted
        while True:
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        print("\n\nStopping conversation...")
    finally:
        await manager.stop_conversation()

    print("\n" + "=" * 60)
    print("✅ Conversation ended")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nExiting...")

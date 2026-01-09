"""
Reachy Mini Companion - Main Application

An AI-powered desk companion that brings Reachy Mini to life with:
- Face detection and recognition
- Natural conversation capabilities
- Expressive emotions and gestures
- Personality and memory

This is the foundation - we'll build it step by step!
"""

import threading
import time
import asyncio
import warnings
import logging
from reachy_mini import ReachyMini, ReachyMiniApp
from reachy_mini.utils import create_head_pose

# Suppress antenna warnings when moves are running (harmless)
# These warnings occur when antenna commands overlap with head movements - expected behavior
# Need to suppress at multiple levels due to app framework logging setup
warnings.filterwarnings("ignore", message=".*Ignoring antennas_joint_positions.*")

# Also configure logging to suppress these warnings
import sys

class SuppressAntennaWarnings(logging.Filter):
    def filter(self, record):
        return "Ignoring antennas_joint_positions" not in record.getMessage()

# Set up logging filter
for handler in logging.root.handlers:
    handler.addFilter(SuppressAntennaWarnings())

# Also apply to specific loggers
logging.getLogger('reachy_mini.daemon.backend.abstract').addFilter(SuppressAntennaWarnings())
logging.getLogger('reachy_mini').addFilter(SuppressAntennaWarnings())

try:
    from .emotions import EmotionManager
    from .movement_manager import MovementManager
    from .conversation_manager import ConversationManager
    from .config import config
except ImportError:
    from emotions import EmotionManager
    from movement_manager import MovementManager
    from conversation_manager import ConversationManager
    from config import config


class ReachyMiniCompanion(ReachyMiniApp):
    """
    AI Companion App for Reachy Mini.

    This app runs in a background thread and makes Reachy Mini
    an interactive desk companion.
    """

    # Optional: URL to custom web interface
    custom_app_url: str | None = None

    def run(self, reachy_mini: ReachyMini, stop_event: threading.Event):
        """
        Main app loop - runs until stop_event is set.

        Args:
            reachy_mini: Pre-initialized ReachyMini instance
            stop_event: Threading event to signal graceful shutdown
        """
        # Apply warning filter again (in case app framework reset logging)
        for handler in logging.root.handlers:
            handler.addFilter(SuppressAntennaWarnings())

        print("🤖 Reachy Mini Companion starting up...")
        print("   Press Stop in dashboard to exit gracefully")

        # Initialize companion (we'll build this step by step)
        self.initialize_companion(reachy_mini)

        # Main loop - runs until user clicks Stop
        while not stop_event.is_set():
            try:
                # Main companion logic will go here
                # For now, just a simple idle behavior
                self.idle_behavior(reachy_mini)

                # Check every 100ms
                time.sleep(0.1)

            except Exception as e:
                print(f"⚠️  Error in companion loop: {e}")
                time.sleep(1)  # Prevent rapid error loops

        # Cleanup when stopping
        print("👋 Reachy Mini Companion shutting down...")
        self.cleanup(reachy_mini)

    def initialize_companion(self, reachy_mini: ReachyMini):
        """
        Initialize the companion's systems.

        We'll add initialization for:
        - Emotion system ✅
        - Movement manager ✅
        - Conversation system ✅
        - Camera/vision system (later)
        - Memory/state (later)
        - Personality traits (later)
        """
        print("   Initializing companion systems...")

        # Store robot reference
        self.robot = reachy_mini

        # Initialize emotion manager
        self.emotion_manager = EmotionManager(reachy_mini, verbose=True)
        print("   ✅ Emotion system ready")

        # Initialize movement manager
        self.movement_manager = MovementManager(reachy_mini, verbose=True)
        print("   ✅ Movement manager ready")

        # Initialize conversation manager
        self.conversation_manager = ConversationManager(
            robot=reachy_mini,
            api_key=config.GEMINI_API_KEY,
            system_instruction=(
                "You are Reachy Mini, a friendly desk companion robot. "
                "You help with tasks, answer questions, and provide companionship. "
                "Keep your responses natural and conversational. "
                "Be brief but helpful."
            ),
            verbose=True,
        )
        print("   ✅ Conversation system ready")

        # Conversation state
        self.conversation_active = False
        self.conversation_thread = None
        self.conversation_loop = None

        # Return to neutral position
        neutral_head = create_head_pose(roll=0, pitch=0, yaw=0)
        reachy_mini.goto_target(head=neutral_head, antennas=[0, 0], duration=1.0)
        time.sleep(1.0)

        # Start movement manager
        self.movement_manager.start()

        # Welcome behavior - Happy emotion to greet the user
        print("\n   👋 Waking up Reachy...")
        self.movement_manager.execute_emotion(
            self.emotion_manager, EmotionManager.HAPPY, with_antennas=True
        )

        print(f"   📋 Queued {self.movement_manager.get_queue_size()} movements")
        print("   ✅ Companion ready!\n")

        # Auto-start conversation
        print("   🎙️  Starting conversation system...")
        self.start_conversation()
        print("   ✅ Conversation active - speak to Reachy!\n")

    def idle_behavior(self, reachy_mini: ReachyMini):
        """
        Idle behavior when companion is not interacting.

        Simple breathing-like motion for now.
        We'll make this more sophisticated later.
        """
        import numpy as np

        # Gentle antenna movement (breathing effect)
        t = time.time()
        antenna_pos = 0.2 * np.sin(2 * np.pi * 0.2 * t)  # Slow oscillation

        reachy_mini.set_target(antennas=[antenna_pos, antenna_pos])

    def start_conversation(self):
        """
        Start a conversation with the robot.

        This creates a separate thread to run the async conversation.
        The robot will show curious emotion while starting.
        """
        if self.conversation_active:
            print("⚠️  Conversation already active")
            return

        print("\n🗣️  Starting conversation...")

        # Show curious emotion
        self.movement_manager.execute_emotion(
            self.emotion_manager,
            EmotionManager.CURIOUS,
            with_antennas=True
        )

        # Run conversation in separate thread with its own event loop
        def run_async_conversation():
            # Create new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            self.conversation_loop = loop

            try:
                # Start conversation
                loop.run_until_complete(self.conversation_manager.start_conversation())

                # Keep loop running
                loop.run_forever()
            except Exception as e:
                print(f"⚠️  Conversation error: {e}")
            finally:
                loop.close()

        self.conversation_thread = threading.Thread(
            target=run_async_conversation,
            daemon=True,
            name="ConversationThread"
        )
        self.conversation_thread.start()
        self.conversation_active = True

        print("✅ Conversation started!\n")

    def stop_conversation(self):
        """
        Stop the current conversation gracefully.
        """
        if not self.conversation_active:
            print("⚠️  No conversation active")
            return

        print("\n🛑 Stopping conversation...")

        # Stop conversation via event loop
        if self.conversation_loop:
            asyncio.run_coroutine_threadsafe(
                self.conversation_manager.stop_conversation(),
                self.conversation_loop
            ).result(timeout=10.0)

            # Stop the event loop
            self.conversation_loop.call_soon_threadsafe(self.conversation_loop.stop)

        # Wait for thread to finish
        if self.conversation_thread:
            self.conversation_thread.join(timeout=5.0)

        self.conversation_active = False
        self.conversation_thread = None
        self.conversation_loop = None

        # Return to neutral emotion
        self.movement_manager.execute_emotion(
            self.emotion_manager,
            "neutral"
        )

        print("✅ Conversation stopped\n")

    def cleanup(self, reachy_mini: ReachyMini):
        """
        Cleanup when app stops.

        Stop conversation and movement manager.
        """
        # Stop conversation if active
        if hasattr(self, 'conversation_active') and self.conversation_active:
            try:
                self.stop_conversation()
            except Exception as e:
                print(f"   ⚠️  Error stopping conversation: {e}")

        # Stop movement manager
        if hasattr(self, 'movement_manager'):
            self.movement_manager.stop()
            print("   ✅ Movement manager stopped")

        print("   ✅ Cleanup complete")


if __name__ == "__main__":
    app = ReachyMiniCompanion()
    try:
        app.wrapped_run()
    except KeyboardInterrupt:
        app.stop()

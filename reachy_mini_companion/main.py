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
from reachy_mini import ReachyMini, ReachyMiniApp
from reachy_mini.utils import create_head_pose

try:
    from .emotions import EmotionManager
except ImportError:
    from emotions import EmotionManager


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
        - Camera/vision system (later)
        - AI/LLM connection (later)
        - Memory/state (later)
        - Personality traits (later)
        """
        print("   Initializing companion systems...")

        # Initialize emotion manager
        self.emotion_manager = EmotionManager(reachy_mini, verbose=True)
        print("   ✅ Emotion system ready")

        # Return to neutral position
        neutral_head = create_head_pose(roll=0, pitch=0, yaw=0)
        reachy_mini.goto_target(head=neutral_head, antennas=[0, 0], duration=1.0)
        time.sleep(1.0)

        print("   ✅ Companion ready!")

        # Test all emotions on startup (remove this later)
        print("\n   🎭 Testing all emotions...")
        print("   Press Ctrl+C anytime to skip to idle mode\n")
        time.sleep(1.0)

        # Test CURIOUS
        print("   [1/4] Testing CURIOUS...")
        self.emotion_manager.show_emotion(EmotionManager.CURIOUS, with_antennas=True)
        time.sleep(1.0)

        # Test HAPPY
        print("   [2/4] Testing HAPPY...")
        self.emotion_manager.show_emotion(EmotionManager.HAPPY, with_antennas=True)
        time.sleep(1.0)

        # Test EXCITED
        print("   [3/4] Testing EXCITED...")
        self.emotion_manager.show_emotion(EmotionManager.EXCITED, with_antennas=False)
        time.sleep(1.0)

        # Test SAD
        print("   [4/4] Testing SAD...")
        self.emotion_manager.show_emotion(EmotionManager.SAD, with_antennas=True)
        time.sleep(1.0)

        # Return to neutral
        print("   ✅ All emotions tested! Returning to neutral...\n")
        self.emotion_manager.neutral()

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

    def cleanup(self, reachy_mini: ReachyMini):
        """
        Cleanup when app stops.

        Return robot to neutral position.
        """
        neutral_head = create_head_pose(roll=0, pitch=0, yaw=0)
        reachy_mini.goto_target(head=neutral_head, antennas=[0, 0], duration=0.5)
        time.sleep(0.5)
        print("   ✅ Cleanup complete")


# For local testing outside of dashboard
if __name__ == "__main__":
    print("🤖 Reachy Mini Companion - Local Testing Mode")
    print("   (In production, this runs via the dashboard)")
    print()

    # Choose mode
    print("Select mode:")
    print("  1 - Simulator (localhost)")
    print("  2 - Real Robot (wireless)")
    mode = input("Enter 1 or 2: ").strip()

    if mode == "1":
        print("\n🎮 Connecting to SIMULATOR...")
        print("   (Make sure simulator daemon is running!)")
        robot = ReachyMini(localhost_only=True, media_backend="no_media")
        print("   ✅ Connected to simulator!")
    elif mode == "2":
        print("\n🤖 Connecting to REAL ROBOT...")
        print("   (Make sure robot is powered on and connected to WiFi!)")
        robot = ReachyMini(localhost_only=False, media_backend="no_media")
        print("   ✅ Connected to real robot!")
    else:
        print("❌ Invalid choice!")
        exit(1)

    # Create stop event for testing
    stop_event = threading.Event()

    # Create and run app
    app = ReachyMiniCompanion()

    try:
        print("   Press Ctrl+C to stop...")
        app.run(robot, stop_event)
    except KeyboardInterrupt:
        print("\n   Stopping...")
        stop_event.set()
        time.sleep(1)

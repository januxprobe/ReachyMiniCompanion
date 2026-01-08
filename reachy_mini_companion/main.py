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
    from .movement_manager import MovementManager
except ImportError:
    from emotions import EmotionManager
    from movement_manager import MovementManager


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
        - Movement manager ✅
        - Camera/vision system (later)
        - AI/LLM connection (later)
        - Memory/state (later)
        - Personality traits (later)
        """
        print("   Initializing companion systems...")

        # Initialize emotion manager
        self.emotion_manager = EmotionManager(reachy_mini, verbose=True)
        print("   ✅ Emotion system ready")

        # Initialize movement manager
        self.movement_manager = MovementManager(reachy_mini, verbose=True)
        print("   ✅ Movement manager ready")

        # Return to neutral position
        neutral_head = create_head_pose(roll=0, pitch=0, yaw=0)
        reachy_mini.goto_target(head=neutral_head, antennas=[0, 0], duration=1.0)
        time.sleep(1.0)

        # Start movement manager
        self.movement_manager.start()

        # Queue startup emotion tests (non-blocking!)
        print("\n   🎭 Queuing startup emotion tests...")
        self.movement_manager.execute_emotion(
            self.emotion_manager, EmotionManager.CURIOUS, with_antennas=True
        )
        self.movement_manager.execute_emotion(
            self.emotion_manager, EmotionManager.HAPPY, with_antennas=True
        )
        self.movement_manager.execute_emotion(
            self.emotion_manager, EmotionManager.EXCITED, with_antennas=False
        )
        self.movement_manager.execute_emotion(
            self.emotion_manager, EmotionManager.SAD, with_antennas=True
        )

        # Queue return to neutral
        def return_neutral(robot):
            self.emotion_manager.neutral()

        self.movement_manager.execute_gesture(
            return_neutral, name="return_to_neutral"
        )

        print(f"   📋 Queued {self.movement_manager.get_queue_size()} movements")
        print("   ✅ Companion ready!\n")

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

        Stop movement manager and return robot to neutral position.
        """
        # Stop movement manager
        if hasattr(self, 'movement_manager'):
            self.movement_manager.stop()
            print("   ✅ Movement manager stopped")

        # Return to neutral position
        neutral_head = create_head_pose(roll=0, pitch=0, yaw=0)
        reachy_mini.goto_target(head=neutral_head, antennas=[0, 0], duration=0.5)
        time.sleep(0.5)
        print("   ✅ Cleanup complete")


if __name__ == "__main__":
    app = ReachyMiniCompanion()
    try:
        app.wrapped_run()
    except KeyboardInterrupt:
        app.stop()

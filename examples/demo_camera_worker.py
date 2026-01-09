#!/usr/bin/env python3
"""
Demo: Camera Worker

Demonstrates the camera worker capturing frames and reporting FPS.

Usage:
    python examples/demo_camera_worker.py
"""

import time
from reachy_mini import ReachyMini
from reachy_mini_companion.camera_worker import CameraWorker


def main():
    """Test camera worker."""
    print("\n" + "=" * 60)
    print("🎥 Camera Worker Demo")
    print("=" * 60)

    # Create robot instance with camera enabled
    print("\nConnecting to robot...")
    robot = ReachyMini(media_backend="default")  # Enables camera and audio

    # Create camera worker
    print("Creating camera worker...")
    camera_worker = CameraWorker(robot, verbose=True)

    print("\n" + "=" * 60)
    print("Starting camera capture...")
    print("=" * 60 + "\n")

    try:
        # Start capturing
        camera_worker.start()

        # Run for 10 seconds
        print("Capturing frames for 10 seconds...")
        print("Watch the FPS counter!\n")

        for i in range(10):
            time.sleep(1)

            # Get latest frame stats
            stats = camera_worker.get_stats()
            frame = camera_worker.get_latest_frame()

            if frame is not None:
                print(f"[{i+1}/10] Frame shape: {frame.shape}, FPS: {stats['fps']:.1f}")
            else:
                print(f"[{i+1}/10] No frame yet...")

    except KeyboardInterrupt:
        print("\n\nStopping...")
    finally:
        # Stop camera
        camera_worker.stop()

    print("\n" + "=" * 60)
    print("✅ Demo Complete")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()

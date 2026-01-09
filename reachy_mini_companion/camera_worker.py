"""
Camera Worker for Reachy Mini

Captures frames from the robot camera in a background thread and tracks FPS.
"""

import time
import threading
import numpy as np
from typing import Optional
from reachy_mini import ReachyMini


class CameraWorker:
    """
    Background worker that continuously captures camera frames.

    Runs in a separate thread and provides:
    - Latest frame access
    - FPS tracking
    - Graceful start/stop
    """

    def __init__(self, robot: ReachyMini, verbose: bool = True):
        """
        Initialize the camera worker.

        Args:
            robot: ReachyMini instance with camera access
            verbose: If True, print status messages
        """
        self.robot = robot
        self.verbose = verbose

        # Frame storage
        self.latest_frame: Optional[np.ndarray] = None
        self.frame_lock = threading.Lock()

        # FPS tracking
        self.frame_count = 0
        self.fps = 0.0
        self.last_fps_time = time.time()

        # Thread control
        self.worker_thread: Optional[threading.Thread] = None
        self.stop_event = threading.Event()
        self.running = False

    def start(self):
        """Start the camera worker thread."""
        if self.running:
            if self.verbose:
                print("[CameraWorker] Already running")
            return

        # Check if camera is available
        try:
            test_frame = self.robot.media.get_frame()
            if test_frame is None:
                if self.verbose:
                    print("[CameraWorker] ⚠️  Camera not available (media_backend may need 'default' instead of 'default_no_video')")
                return
        except Exception as e:
            if self.verbose:
                print(f"[CameraWorker] ⚠️  Camera not available: {e}")
            return

        if self.verbose:
            print("[CameraWorker] Starting camera worker...")

        self.stop_event.clear()
        self.running = True

        self.worker_thread = threading.Thread(
            target=self._capture_loop,
            daemon=True,
            name="CameraWorker"
        )
        self.worker_thread.start()

        if self.verbose:
            print("[CameraWorker] ✅ Camera worker started")

    def stop(self):
        """Stop the camera worker thread."""
        if not self.running:
            if self.verbose:
                print("[CameraWorker] Not running")
            return

        if self.verbose:
            print("[CameraWorker] Stopping camera worker...")

        self.stop_event.set()
        self.running = False

        if self.worker_thread:
            self.worker_thread.join(timeout=2.0)

        if self.verbose:
            print(f"[CameraWorker] ✅ Stopped (captured {self.frame_count} frames)")

    def _capture_loop(self):
        """Main capture loop (runs in background thread)."""
        try:
            while not self.stop_event.is_set():
                try:
                    # Capture frame
                    frame = self.robot.media.get_frame()

                    if frame is not None:
                        # Store frame (thread-safe)
                        with self.frame_lock:
                            self.latest_frame = frame
                            self.frame_count += 1

                        # Update FPS every second
                        current_time = time.time()
                        if current_time - self.last_fps_time >= 1.0:
                            self.fps = self.frame_count / (current_time - self.last_fps_time)
                            self.frame_count = 0
                            self.last_fps_time = current_time

                            if self.verbose:
                                print(f"[CameraWorker] FPS: {self.fps:.1f}")

                    # Small sleep to prevent busy waiting
                    time.sleep(0.01)  # ~100 FPS max

                except Exception as e:
                    if self.verbose:
                        print(f"[CameraWorker] ⚠️  Error capturing frame: {e}")
                    time.sleep(0.1)

        except Exception as e:
            if self.verbose:
                print(f"[CameraWorker] ⚠️  Capture loop error: {e}")

    def get_latest_frame(self) -> Optional[np.ndarray]:
        """
        Get the most recent camera frame (thread-safe).

        Returns:
            Latest frame as numpy array, or None if no frame captured yet
        """
        with self.frame_lock:
            return self.latest_frame.copy() if self.latest_frame is not None else None

    def get_fps(self) -> float:
        """Get current FPS."""
        return self.fps

    def get_stats(self) -> dict:
        """
        Get camera worker statistics.

        Returns:
            Dictionary with fps and frame info
        """
        with self.frame_lock:
            frame_shape = self.latest_frame.shape if self.latest_frame is not None else None

        return {
            "fps": self.fps,
            "running": self.running,
            "frame_shape": frame_shape,
        }

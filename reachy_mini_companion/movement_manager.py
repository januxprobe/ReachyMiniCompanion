"""
Movement Manager - Threaded Movement Orchestration

Manages robot movements in a background thread with queue-based execution.
Supports emotions, gestures, and idle behaviors with priority handling.
"""

import threading
import queue
import time
from enum import Enum
from typing import Optional, Callable
from reachy_mini import ReachyMini


class Priority(Enum):
    """Movement priority levels."""
    HIGH = 1    # Interrupts current movement (safety, user commands)
    NORMAL = 2  # Standard movements (emotions, gestures)
    LOW = 3     # Background behaviors (idle animations)


class MovementCommand:
    """Represents a movement command to be executed."""

    def __init__(
        self,
        name: str,
        function: Callable,
        priority: Priority = Priority.NORMAL,
        interruptible: bool = True
    ):
        """
        Create a movement command.

        Args:
            name: Human-readable name for logging
            function: Function to execute (takes robot as argument)
            priority: Command priority level
            interruptible: Whether this movement can be interrupted
        """
        self.name = name
        self.function = function
        self.priority = priority
        self.interruptible = interruptible
        self.timestamp = time.time()

    def __lt__(self, other):
        """Compare by priority for priority queue."""
        return self.priority.value < other.priority.value


class MovementManager:
    """
    Manages robot movements in a background thread.

    Features:
    - Non-blocking movement execution
    - Priority-based command queuing
    - Graceful interruption
    - Idle behavior support
    """

    def __init__(self, robot: ReachyMini, verbose: bool = False):
        """
        Initialize the movement manager.

        Args:
            robot: ReachyMini instance to control
            verbose: Enable verbose logging
        """
        self.robot = robot
        self.verbose = verbose

        # Command queue (priority queue)
        self.command_queue = queue.PriorityQueue()

        # Thread control
        self.worker_thread: Optional[threading.Thread] = None
        self.stop_flag = threading.Event()
        self.interrupt_flag = threading.Event()

        # Current state
        self.current_command: Optional[MovementCommand] = None
        self.is_running = False

        # Idle behavior
        self.idle_behavior: Optional[Callable] = None
        self.idle_enabled = False

    def start(self):
        """Start the movement manager background thread."""
        if self.is_running:
            self._log("⚠️  Movement manager already running")
            return

        self._log("🎬 Starting movement manager")
        self.stop_flag.clear()
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker_thread.start()
        self.is_running = True
        self._log("✅ Movement manager started")

    def stop(self, timeout: float = 5.0):
        """
        Stop the movement manager gracefully.

        Args:
            timeout: Maximum time to wait for thread to finish
        """
        if not self.is_running:
            return

        self._log("🛑 Stopping movement manager")
        self.stop_flag.set()

        if self.worker_thread:
            self.worker_thread.join(timeout=timeout)
            if self.worker_thread.is_alive():
                self._log("⚠️  Movement manager did not stop gracefully")
            else:
                self._log("✅ Movement manager stopped")

        self.is_running = False

    def execute_emotion(
        self,
        emotion_manager,
        emotion_name: str,
        with_antennas: bool = True,
        priority: Priority = Priority.NORMAL
    ):
        """
        Queue an emotion to be executed.

        Args:
            emotion_manager: EmotionManager instance
            emotion_name: Name of emotion (use EmotionManager constants)
            with_antennas: Include antenna movements
            priority: Command priority
        """
        def emotion_func(robot):
            emotion_manager.show_emotion(emotion_name, with_antennas)

        command = MovementCommand(
            name=f"emotion:{emotion_name}",
            function=emotion_func,
            priority=priority,
            interruptible=True
        )

        self._queue_command(command)

    def execute_gesture(
        self,
        gesture_func: Callable,
        name: str = "gesture",
        priority: Priority = Priority.NORMAL
    ):
        """
        Queue a custom gesture to be executed.

        Args:
            gesture_func: Function that performs the gesture (takes robot)
            name: Human-readable name for logging
            priority: Command priority
        """
        command = MovementCommand(
            name=name,
            function=gesture_func,
            priority=priority,
            interruptible=True
        )

        self._queue_command(command)

    def set_idle_behavior(self, behavior_func: Optional[Callable], enabled: bool = True):
        """
        Set the idle behavior (runs when no commands in queue).

        Args:
            behavior_func: Function to call when idle (takes robot, returns quickly)
            enabled: Enable/disable idle behavior
        """
        self.idle_behavior = behavior_func
        self.idle_enabled = enabled
        self._log(f"🌙 Idle behavior {'enabled' if enabled else 'disabled'}")

    def interrupt_current(self):
        """Interrupt the currently executing movement."""
        if self.current_command and self.current_command.interruptible:
            self._log(f"⏸️  Interrupting: {self.current_command.name}")
            self.interrupt_flag.set()

    def clear_queue(self):
        """Clear all pending commands from the queue."""
        while not self.command_queue.empty():
            try:
                self.command_queue.get_nowait()
            except queue.Empty:
                break
        self._log("🗑️  Command queue cleared")

    def get_queue_size(self) -> int:
        """Get the number of pending commands."""
        return self.command_queue.qsize()

    # Private methods

    def _queue_command(self, command: MovementCommand):
        """Add a command to the queue."""
        self.command_queue.put(command)
        self._log(f"📥 Queued: {command.name} (priority: {command.priority.name})")

    def _worker_loop(self):
        """Main worker thread loop - processes commands from queue."""
        self._log("🔄 Worker thread started")

        while not self.stop_flag.is_set():
            try:
                # Try to get a command (timeout allows checking stop_flag)
                try:
                    command = self.command_queue.get(timeout=0.1)
                except queue.Empty:
                    # No commands - run idle behavior if enabled
                    if self.idle_enabled and self.idle_behavior:
                        self.idle_behavior(self.robot)
                    continue

                # Execute the command
                self._execute_command(command)

            except Exception as e:
                self._log(f"⚠️  Error in worker loop: {e}")
                time.sleep(0.1)  # Prevent rapid error loops

        self._log("🔄 Worker thread stopped")

    def _execute_command(self, command: MovementCommand):
        """Execute a single command."""
        self.current_command = command
        self.interrupt_flag.clear()

        self._log(f"▶️  Executing: {command.name}")

        try:
            # Execute the movement function
            command.function(self.robot)
            self._log(f"✅ Completed: {command.name}")

        except Exception as e:
            self._log(f"❌ Error executing {command.name}: {e}")

        finally:
            self.current_command = None
            self.interrupt_flag.clear()

    def _log(self, message: str):
        """Log a message if verbose mode is enabled."""
        if self.verbose:
            print(f"[MovementManager] {message}")

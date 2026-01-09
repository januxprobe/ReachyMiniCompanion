"""
Conversation Manager for Reachy Mini ↔ Gemini Live API

This module manages real-time bidirectional audio streaming between
the Reachy Mini robot and Google's Gemini Live API.

Based on the official Google Gemini Live API example.

Key Features:
- Bidirectional audio streaming (microphone → Gemini → speakers)
- Automatic format conversion (stereo ↔ mono, 16kHz ↔ 24kHz)
- Interruption handling (user can interrupt AI mid-response)
- Queue-based buffering for smooth audio flow
- Async/await with separate tasks for each operation

Architecture:
    Robot Microphone → Listen Task → Queue → Send Task → Gemini Live API
                                                                ↓
    Robot Speakers ← Play Task ← Queue ← Receive Task ← Gemini Live API

All tasks run concurrently in an asyncio TaskGroup.
"""

import asyncio
import time
import numpy as np
from typing import Optional
from google import genai
from reachy_mini import ReachyMini
from reachy_mini_companion.audio_converters import (
    prepare_for_gemini,
    prepare_from_gemini,
)


class ConversationManager:
    """
    Manages a live conversation between Reachy Mini and Gemini.

    Based on the official Google Gemini Live API example, adapted for ReachyMini.

    Usage:
        ```python
        robot = ReachyMini(media_backend="default_no_video")
        manager = ConversationManager(robot, api_key="your_key")

        await manager.run_conversation(duration_seconds=30)
        ```
    """

    def __init__(
        self,
        robot: ReachyMini,
        api_key: str,
        model: str = "gemini-2.0-flash-exp",
        system_instruction: Optional[str] = None,
        verbose: bool = True,
    ):
        """
        Initialize the conversation manager.

        Args:
            robot: ReachyMini instance with audio enabled
            api_key: Google Gemini API key
            model: Gemini model to use
            system_instruction: Optional system prompt for Gemini
            verbose: Print debug information
        """
        self.robot = robot
        self.api_key = api_key
        self.model = model
        self.verbose = verbose

        # Default system instruction
        if system_instruction is None:
            self.system_instruction = (
                "You are Reachy Mini, a friendly desk companion robot. "
                "You help with tasks, answer questions, and provide companionship. "
                "Keep your responses natural and conversational. "
                "Be brief but helpful."
            )
        else:
            self.system_instruction = system_instruction

        # Gemini client
        self.client = genai.Client(api_key=api_key)

        # Audio queues (like the official example)
        self.audio_queue_mic = asyncio.Queue(maxsize=5)
        self.audio_queue_output = asyncio.Queue()

        # Conversation control
        self._conversation_task: Optional[asyncio.Task] = None
        self._stop_event = asyncio.Event()

        # Statistics
        self.stats = {
            "input_chunks_sent": 0,
            "output_chunks_received": 0,
            "interruptions": 0,
            "errors": 0,
            "session_start_time": None,
        }

    def _log(self, message: str):
        """Log a message if verbose is enabled."""
        if self.verbose:
            print(f"[ConversationManager] {message}")

    async def listen_audio(self):
        """
        Listen to robot microphone and put audio into the mic queue.
        Based on the official Google example's listen_audio function.
        """
        self._log("🎤 Listening to microphone...")
        try:
            while True:
                # Get audio from robot microphone
                audio_chunk = self.robot.media.audio.get_audio_sample()

                if audio_chunk is not None:
                    # Handle both stereo and mono audio
                    if audio_chunk.ndim == 1 or (audio_chunk.ndim == 2 and audio_chunk.shape[1] == 1):
                        # Mono audio - convert to stereo
                        if audio_chunk.ndim == 2:
                            audio_chunk = audio_chunk.squeeze()
                        audio_chunk = np.column_stack([audio_chunk, audio_chunk]).astype(np.float32)

                    # Convert to Gemini format (mono 16kHz PCM)
                    pcm_bytes, mime_type = prepare_for_gemini(audio_chunk)

                    # Put into queue (like official example)
                    await self.audio_queue_mic.put({"data": pcm_bytes, "mime_type": "audio/pcm"})

                # Small delay to match audio sampling rate
                await asyncio.sleep(0.01)

        except asyncio.CancelledError:
            self._log("Listen task cancelled")
            raise

    async def send_realtime(self, session):
        """
        Send audio from mic queue to Gemini session.
        Based on the official Google example's send_realtime function.
        """
        self._log("📤 Sending audio to Gemini...")
        try:
            while True:
                msg = await self.audio_queue_mic.get()
                await session.send_realtime_input(audio=msg)
                self.stats["input_chunks_sent"] += 1

                # Log progress every 500 chunks
                if self.verbose and self.stats["input_chunks_sent"] % 500 == 0:
                    self._log(f"Sent {self.stats['input_chunks_sent']} audio chunks")

        except asyncio.CancelledError:
            self._log("Send task cancelled")
            raise

    async def receive_audio(self, session):
        """
        Receive responses from Gemini and put audio into output queue.
        Based on the official Google example's receive_audio function.
        """
        self._log("📥 Receiving audio from Gemini...")
        try:
            while True:
                # This is the key difference from our old code!
                # Official example does: turn = session.receive()
                turn = session.receive()
                async for response in turn:
                    if response.server_content and response.server_content.model_turn:
                        for part in response.server_content.model_turn.parts:
                            if part.inline_data and isinstance(part.inline_data.data, bytes):
                                # Put audio bytes into output queue
                                self.audio_queue_output.put_nowait(part.inline_data.data)
                                self.stats["output_chunks_received"] += 1

                    # Check for interruption
                    if response.server_content and response.server_content.interrupted:
                        self._log("⚠️  User interrupted (clearing output queue)")
                        self.stats["interruptions"] += 1
                        # Empty the queue on interruption to stop playback
                        while not self.audio_queue_output.empty():
                            self.audio_queue_output.get_nowait()

                    # Check for turn complete
                    if response.server_content and response.server_content.turn_complete:
                        self._log("✅ AI response complete")

        except asyncio.CancelledError:
            self._log("Receive task cancelled")
            raise

    async def play_audio(self):
        """
        Play audio from output queue through robot speakers.
        Based on the official Google example's play_audio function.
        """
        self._log("🔊 Playing audio through speakers...")
        try:
            while True:
                # Get audio bytes from queue
                bytestream = await self.audio_queue_output.get()

                # Convert from Gemini format (24kHz mono PCM) to robot format (48kHz stereo)
                robot_audio = prepare_from_gemini(bytestream, sample_rate=24000, target_sample_rate=48000)

                # Play through speakers
                self.robot.media.audio.push_audio_sample(robot_audio)

        except asyncio.CancelledError:
            self._log("Play task cancelled")
            raise

    def _print_session_stats(self):
        """Print session statistics."""
        duration = time.time() - self.stats["session_start_time"]
        print("\n" + "=" * 60)
        print("📊 Conversation Session Statistics")
        print("=" * 60)
        print(f"Duration: {duration:.1f} seconds")
        print(f"Input chunks sent: {self.stats['input_chunks_sent']:,}")
        print(f"Output chunks received: {self.stats['output_chunks_received']:,}")
        print(f"Interruptions: {self.stats['interruptions']}")
        print(f"Errors: {self.stats['errors']}")

        # Calculate rates
        if duration > 0:
            input_rate = self.stats["input_chunks_sent"] / duration
            output_rate = self.stats["output_chunks_received"] / duration
            print(f"Input rate: {input_rate:.1f} chunks/sec")
            print(f"Output rate: {output_rate:.1f} chunks/sec")

        print("=" * 60 + "\n")

    async def run_conversation(self, duration_seconds: Optional[float] = None, initial_greeting: bool = False):
        """
        Run a conversation for a specified duration.

        This follows the official Google example pattern with separate tasks.

        Args:
            duration_seconds: How long to run (None = infinite)
            initial_greeting: If True, Gemini will greet first
        """
        # Reset statistics
        self.stats["session_start_time"] = time.time()
        self.stats["input_chunks_sent"] = 0
        self.stats["output_chunks_received"] = 0
        self.stats["interruptions"] = 0

        # Start robot audio
        self._log("Starting robot audio system...")
        self.robot.media.audio.start_recording()
        self.robot.media.audio.start_playing()

        # Configure Gemini session (minimal config like official example)
        config = {
            "response_modalities": ["AUDIO"],
            "system_instruction": self.system_instruction,
        }

        self._log(f"Connecting to {self.model}...")

        try:
            # Connect to Gemini Live API
            async with self.client.aio.live.connect(model=self.model, config=config) as session:
                self._log("✅ Connected to Gemini Live API!")

                # Send initial greeting if requested
                if initial_greeting:
                    self._log("👋 Sending greeting request...")
                    await session.send(input="Say hello and introduce yourself as Reachy Mini, a friendly desk companion. Keep it brief.", end_of_turn=True)

                self._log("🎙️  Conversation active! Speak to the robot.")

                # Run all tasks in a TaskGroup (like official example)
                try:
                    async with asyncio.TaskGroup() as tg:
                        # Create all tasks
                        tg.create_task(self.listen_audio())
                        tg.create_task(self.send_realtime(session))
                        tg.create_task(self.receive_audio(session))
                        tg.create_task(self.play_audio())

                        # If duration specified, create a timeout task
                        if duration_seconds:
                            async def timeout():
                                await asyncio.sleep(duration_seconds)
                                raise asyncio.CancelledError("Duration completed")
                            tg.create_task(timeout())
                        else:
                            # Run until stop_event is set
                            self._log("Running conversation (press Ctrl+C to stop)...")
                            async def run_until_stopped():
                                while not self._stop_event.is_set():
                                    await asyncio.sleep(0.1)
                                raise asyncio.CancelledError("Stopped by user")
                            tg.create_task(run_until_stopped())

                except asyncio.CancelledError:
                    self._log("Conversation ending...")

        except KeyboardInterrupt:
            self._log("Interrupted by user")
        finally:
            # Stop robot audio
            self.robot.media.audio.stop_recording()
            self.robot.media.audio.stop_playing()

            # Print statistics
            if self.verbose:
                self._print_session_stats()

            self._log("✅ Conversation stopped")

    async def start_conversation(self, with_greeting: bool = False):
        """
        Start a conversation session.

        Creates a background task that runs the conversation until stopped.
        Use stop_conversation() to end the conversation gracefully.

        Args:
            with_greeting: If True, Gemini will greet first
        """
        if self._conversation_task is not None and not self._conversation_task.done():
            self._log("⚠️  Conversation already running")
            return

        self._log("Starting conversation...")

        # Clear stop event
        self._stop_event.clear()

        # Create conversation task with greeting option
        self._conversation_task = asyncio.create_task(self.run_conversation(initial_greeting=with_greeting))

        self._log("✅ Conversation started")

    async def stop_conversation(self):
        """
        Stop the current conversation session gracefully.

        Signals the conversation to stop and waits for cleanup.
        """
        if self._conversation_task is None:
            self._log("⚠️  No conversation running")
            return

        self._log("Stopping conversation...")

        # Signal stop
        self._stop_event.set()

        # Wait for task to finish (with timeout)
        try:
            await asyncio.wait_for(self._conversation_task, timeout=5.0)
        except asyncio.TimeoutError:
            self._log("⚠️  Conversation didn't stop gracefully, cancelling...")
            self._conversation_task.cancel()
            try:
                await self._conversation_task
            except asyncio.CancelledError:
                pass

        self._conversation_task = None
        self._log("✅ Conversation stopped")


# Convenience function for quick testing
async def run_conversation_test(
    duration_seconds: float = 30.0,
    api_key: Optional[str] = None,
    verbose: bool = True,
):
    """
    Quick test of the conversation system.

    Args:
        duration_seconds: How long to run the conversation
        api_key: Gemini API key (if None, loads from config)
        verbose: Print debug information

    Usage:
        ```python
        import asyncio
        from reachy_mini_companion.conversation_manager import run_conversation_test

        asyncio.run(run_conversation_test(duration_seconds=30))
        ```
    """
    from reachy_mini_companion.config import config

    if api_key is None:
        api_key = config.GEMINI_API_KEY

    print("=" * 60)
    print("🤖 Reachy Mini Conversation Test")
    print("=" * 60)
    print(f"Duration: {duration_seconds} seconds")
    print("Speak to the robot to start a conversation!")
    print("=" * 60 + "\n")

    # Create robot instance (audio only, no video)
    robot = ReachyMini(media_backend="default_no_video")

    # Create conversation manager
    manager = ConversationManager(
        robot=robot,
        api_key=api_key,
        verbose=verbose,
    )

    # Run conversation
    await manager.run_conversation(duration_seconds=duration_seconds)

    print("\n" + "=" * 60)
    print("✅ Conversation test complete!")
    print("=" * 60)

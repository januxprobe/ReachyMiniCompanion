"""
Emotion System for Reachy Mini Companion

Provides expressive emotions combining head movements and antenna gestures.
"""

import time
from reachy_mini import ReachyMini
from reachy_mini.utils import create_head_pose


# ============================================================
# EMOTION FUNCTIONS
# ============================================================

def show_happy(robot: ReachyMini, verbose: bool = False):
    """
    Express happiness - looking up with antennas raised.

    Args:
        robot: ReachyMini robot instance
        verbose: If True, print status messages
    """
    if verbose:
        print("😊 Showing HAPPY emotion!")

    head_pose = create_head_pose(roll=0, pitch=15, yaw=0)
    robot.goto_target(
        head=head_pose,
        antennas=[0.8, 0.8],
        duration=0.5
    )
    time.sleep(0.5)

    if verbose:
        print("   Done!")


def show_sad(robot: ReachyMini, verbose: bool = False):
    """
    Express sadness - looking down with droopy antennas.

    Args:
        robot: ReachyMini robot instance
        verbose: If True, print status messages
    """
    if verbose:
        print("😢 Showing SAD emotion...")

    head_pose = create_head_pose(roll=0, pitch=-20, yaw=0)
    robot.goto_target(
        head=head_pose,
        antennas=[-0.8, -0.8],
        duration=0.8
    )
    time.sleep(0.8)

    if verbose:
        print("   Done!")


def show_excited(robot: ReachyMini, verbose: bool = False):
    """
    Express excitement - fast nodding with wiggling antennas.

    Args:
        robot: ReachyMini robot instance
        verbose: If True, print status messages
    """
    if verbose:
        print("🤩 Showing EXCITED emotion!")

    for _ in range(3):
        # Nod up
        head_up = create_head_pose(roll=0, pitch=10, yaw=0)
        robot.goto_target(head=head_up, antennas=[1.0, -1.0], duration=0.2)
        time.sleep(0.2)

        # Nod down
        head_down = create_head_pose(roll=0, pitch=-10, yaw=0)
        robot.goto_target(head=head_down, antennas=[-1.0, 1.0], duration=0.2)
        time.sleep(0.2)

    # Return to neutral
    neutral_head = create_head_pose(0, 0, 0)
    robot.goto_target(head=neutral_head, antennas=[0, 0], duration=0.3)
    time.sleep(0.3)

    if verbose:
        print("   Done!")


def show_curious(robot: ReachyMini, verbose: bool = False):
    """
    Express curiosity - tilting head side to side.

    Args:
        robot: ReachyMini robot instance
        verbose: If True, print status messages
    """
    if verbose:
        print("🤔 Showing CURIOUS emotion!")

    # Define head poses
    head_right = create_head_pose(roll=20, pitch=5, yaw=0)
    head_left = create_head_pose(roll=-20, pitch=5, yaw=0)

    # Tilt right
    robot.goto_target(head=head_right, antennas=[0.6, -0.3], duration=0.6)
    time.sleep(0.6)

    # Tilt left
    robot.goto_target(head=head_left, antennas=[-0.3, 0.6], duration=0.6)
    time.sleep(0.6)

    # Tilt right again
    robot.goto_target(head=head_right, antennas=[0.6, -0.3], duration=0.6)
    time.sleep(0.6)

    # Return to neutral
    neutral_head = create_head_pose(0, 0, 0)
    robot.goto_target(head=neutral_head, antennas=[0, 0], duration=0.5)
    time.sleep(0.5)

    if verbose:
        print("   Done!")


# ============================================================
# ANTENNA BEHAVIORS
# ============================================================

def antennas_curious_wave(robot: ReachyMini, verbose: bool = False):
    """
    Wave antennas in a friendly greeting pattern for curious emotion.

    Creates an enthusiastic, welcoming wave by alternating antenna positions
    in a quick, energetic pattern.

    Args:
        robot: ReachyMini robot instance
        verbose: If True, print status messages
    """
    try:
        # Quick alternating wave pattern (3 waves)
        for _ in range(3):
            # Wave up (left up, right down)
            robot.goto_target(antennas=[0.9, -0.5], duration=0.15)
            time.sleep(0.15)

            # Wave alternate (left down, right up)
            robot.goto_target(antennas=[-0.5, 0.9], duration=0.15)
            time.sleep(0.15)

        # Return to neutral
        robot.goto_target(antennas=[0, 0], duration=0.2)
        time.sleep(0.2)

        if verbose:
            print("   👋 Curious antenna wave completed!")

    except Exception as e:
        if verbose:
            print(f"   ⚠️ Curious antenna error: {e}")


def antennas_happy_bounce(robot: ReachyMini, verbose: bool = False):
    """
    Bounce antennas excitedly for happy emotion.

    Creates a joyful, bouncy pattern with both antennas moving up together
    in quick succession, expressing excitement and happiness.

    Args:
        robot: ReachyMini robot instance
        verbose: If True, print status messages
    """
    try:
        # Excited bouncing pattern (3 bounces)
        for _ in range(3):
            # Bounce up together
            robot.goto_target(antennas=[1.0, 1.0], duration=0.2)
            time.sleep(0.2)

            # Down together
            robot.goto_target(antennas=[0.3, 0.3], duration=0.2)
            time.sleep(0.2)

        # End high and happy
        robot.goto_target(antennas=[0.8, 0.8], duration=0.3)
        time.sleep(0.3)

        if verbose:
            print("   😊 Happy antenna bounce completed!")

    except Exception as e:
        if verbose:
            print(f"   ⚠️ Happy antenna error: {e}")


def antennas_sad_droop(robot: ReachyMini, verbose: bool = False):
    """
    Slowly droop antennas for sad emotion.

    Creates a melancholic wilting pattern where antennas slowly lower,
    expressing sadness and disappointment.

    Args:
        robot: ReachyMini robot instance
        verbose: If True, print status messages
    """
    try:
        # Slow wilting pattern
        # Start from neutral
        robot.goto_target(antennas=[0, 0], duration=0.3)
        time.sleep(0.3)

        # Droop down slowly
        robot.goto_target(antennas=[-0.5, -0.5], duration=0.6)
        time.sleep(0.6)

        # Droop even lower
        robot.goto_target(antennas=[-0.8, -0.8], duration=0.6)
        time.sleep(0.6)

        if verbose:
            print("   😢 Sad antenna droop completed!")

    except Exception as e:
        if verbose:
            print(f"   ⚠️ Sad antenna error: {e}")


# ============================================================
# EMOTION MANAGER
# ============================================================

class EmotionManager:
    """
    Manages emotion expressions and antenna behaviors for Reachy Mini.

    Provides a clean interface for triggering emotions and gestures,
    with support for verbose output and error handling.
    """

    # Emotion name constants
    HAPPY = "happy"
    SAD = "sad"
    EXCITED = "excited"
    CURIOUS = "curious"

    def __init__(self, robot: ReachyMini, verbose: bool = False):
        """
        Initialize the emotion manager.

        Args:
            robot: ReachyMini robot instance
            verbose: If True, print status messages
        """
        self.robot = robot
        self.verbose = verbose

        # Map emotion names to functions
        self._emotions = {
            self.HAPPY: show_happy,
            self.SAD: show_sad,
            self.EXCITED: show_excited,
            self.CURIOUS: show_curious,
        }

        # Map emotion names to antenna behaviors
        self._antenna_behaviors = {
            self.HAPPY: antennas_happy_bounce,
            self.SAD: antennas_sad_droop,
            self.CURIOUS: antennas_curious_wave,
        }

    def show_emotion(self, emotion_name: str, with_antennas: bool = True):
        """
        Show an emotion with optional antenna behavior.

        Args:
            emotion_name: Name of the emotion (use class constants)
            with_antennas: If True, also perform antenna behavior

        Returns:
            bool: True if successful, False otherwise
        """
        if emotion_name not in self._emotions:
            if self.verbose:
                print(f"⚠️ Unknown emotion: {emotion_name}")
            return False

        try:
            # Show the emotion
            self._emotions[emotion_name](self.robot, verbose=self.verbose)

            # Optionally add antenna behavior
            if with_antennas and emotion_name in self._antenna_behaviors:
                time.sleep(0.2)  # Small pause between emotion and antenna
                self._antenna_behaviors[emotion_name](self.robot, verbose=self.verbose)

            return True

        except Exception as e:
            if self.verbose:
                print(f"⚠️ Error showing emotion {emotion_name}: {e}")
            return False

    def antenna_gesture(self, emotion_name: str):
        """
        Perform just the antenna gesture for an emotion.

        Args:
            emotion_name: Name of the emotion

        Returns:
            bool: True if successful, False otherwise
        """
        if emotion_name not in self._antenna_behaviors:
            if self.verbose:
                print(f"⚠️ No antenna behavior for: {emotion_name}")
            return False

        try:
            self._antenna_behaviors[emotion_name](self.robot, verbose=self.verbose)
            return True

        except Exception as e:
            if self.verbose:
                print(f"⚠️ Error with antenna gesture {emotion_name}: {e}")
            return False

    def neutral(self):
        """
        Return robot to neutral position.
        """
        try:
            neutral_head = create_head_pose(roll=0, pitch=0, yaw=0)
            self.robot.goto_target(head=neutral_head, antennas=[0, 0], duration=0.5)
            time.sleep(0.5)
            return True

        except Exception as e:
            if self.verbose:
                print(f"⚠️ Error returning to neutral: {e}")
            return False

    def available_emotions(self):
        """
        Get list of available emotions.

        Returns:
            list: List of emotion names
        """
        return list(self._emotions.keys())

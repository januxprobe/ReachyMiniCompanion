"""
Audio format conversion utilities for Reachy Mini ↔ Gemini Live API.

This module handles the audio format conversions needed to bridge between:
- Robot audio: 16kHz stereo (2 channels), float32, normalized [-1.0, 1.0]
- Gemini input: 16kHz mono (1 channel), 16-bit PCM
- Gemini output: 24kHz mono (1 channel), raw PCM

Key conversions:
1. Stereo → Mono (for sending to Gemini)
2. Mono → Stereo (for receiving from Gemini)
3. 24kHz → 16kHz resampling (for Gemini output)
4. Float32 ↔ 16-bit PCM (for API compatibility)
"""

import numpy as np
from scipy import signal
from typing import Tuple


def stereo_to_mono(stereo_audio: np.ndarray) -> np.ndarray:
    """
    Convert stereo (2 channels) to mono (1 channel) by averaging.

    Args:
        stereo_audio: Stereo audio array
            - Shape: (num_samples, 2)
            - dtype: float32
            - Values: -1.0 to 1.0 (normalized)

    Returns:
        Mono audio array
            - Shape: (num_samples,)
            - dtype: float32
            - Values: -1.0 to 1.0 (normalized)

    Example:
        >>> stereo = np.array([[0.5, 0.3], [0.2, 0.4], [-0.1, 0.1]])
        >>> mono = stereo_to_mono(stereo)
        >>> mono.shape
        (3,)
        >>> mono[0]
        0.4  # Average of 0.5 and 0.3
    """
    if stereo_audio.ndim != 2 or stereo_audio.shape[1] != 2:
        raise ValueError(
            f"Expected stereo audio with shape (samples, 2), got {stereo_audio.shape}"
        )

    # Average the two channels
    return stereo_audio.mean(axis=1).astype(np.float32)


def mono_to_stereo(mono_audio: np.ndarray) -> np.ndarray:
    """
    Convert mono (1 channel) to stereo (2 channels) by duplicating.

    Args:
        mono_audio: Mono audio array
            - Shape: (num_samples,)
            - dtype: float32
            - Values: -1.0 to 1.0 (normalized)

    Returns:
        Stereo audio array
            - Shape: (num_samples, 2)
            - dtype: float32
            - Values: -1.0 to 1.0 (normalized)

    Example:
        >>> mono = np.array([0.5, 0.2, -0.1])
        >>> stereo = mono_to_stereo(mono)
        >>> stereo.shape
        (3, 2)
        >>> stereo[0]
        array([0.5, 0.5])
    """
    if mono_audio.ndim != 1:
        raise ValueError(
            f"Expected mono audio with shape (samples,), got {mono_audio.shape}"
        )

    # Duplicate the mono channel to create stereo
    return np.column_stack([mono_audio, mono_audio]).astype(np.float32)


def resample_24k_to_16k(audio_24k: np.ndarray) -> np.ndarray:
    """
    Resample audio from 24kHz to 16kHz.

    Gemini outputs 24kHz audio, but Reachy Mini uses 16kHz.
    This function downsamples by a factor of 1.5 (24000/16000).

    Args:
        audio_24k: Audio at 24kHz sample rate
            - Shape: (num_samples,) for mono
            - dtype: float32
            - Values: -1.0 to 1.0 (normalized)

    Returns:
        Audio at 16kHz sample rate
            - Shape: (num_samples * 2 // 3,)
            - dtype: float32
            - Values: -1.0 to 1.0 (normalized)

    Example:
        >>> audio_24k = np.sin(2 * np.pi * 440 * np.arange(24000) / 24000)
        >>> audio_16k = resample_24k_to_16k(audio_24k)
        >>> len(audio_16k)
        16000
    """
    if audio_24k.ndim != 1:
        raise ValueError(
            f"Expected mono audio with shape (samples,), got {audio_24k.shape}"
        )

    # Calculate new length: 24000 -> 16000 means 2/3 of original
    num_samples_16k = len(audio_24k) * 2 // 3

    # Use scipy's resample (uses FFT, high quality)
    audio_16k = signal.resample(audio_24k, num_samples_16k)

    return audio_16k.astype(np.float32)


def float32_to_pcm16(audio_float: np.ndarray) -> bytes:
    """
    Convert normalized float32 audio to 16-bit PCM bytes.

    This is needed for sending audio to Gemini Live API, which expects
    raw 16-bit PCM format.

    Args:
        audio_float: Normalized float32 audio
            - Shape: (num_samples,) for mono or (num_samples, channels) for multi-channel
            - dtype: float32
            - Values: -1.0 to 1.0 (normalized)

    Returns:
        Raw bytes in 16-bit PCM format (little-endian)

    Example:
        >>> audio = np.array([0.0, 0.5, -0.5, 1.0, -1.0], dtype=np.float32)
        >>> pcm_bytes = float32_to_pcm16(audio)
        >>> len(pcm_bytes)
        10  # 5 samples * 2 bytes per sample
    """
    # Clip to [-1.0, 1.0] range to prevent overflow
    audio_clipped = np.clip(audio_float, -1.0, 1.0)

    # Scale to int16 range: [-32768, 32767]
    audio_int16 = (audio_clipped * 32767).astype(np.int16)

    # Convert to bytes (little-endian)
    return audio_int16.tobytes()


def pcm16_to_float32(pcm_bytes: bytes, num_channels: int = 1) -> np.ndarray:
    """
    Convert 16-bit PCM bytes to normalized float32 audio.

    This is needed for receiving audio from Gemini Live API, which sends
    raw 16-bit PCM format.

    Args:
        pcm_bytes: Raw bytes in 16-bit PCM format (little-endian)
        num_channels: Number of audio channels (1 for mono, 2 for stereo)

    Returns:
        Normalized float32 audio
            - Shape: (num_samples,) for mono or (num_samples, channels) for multi-channel
            - dtype: float32
            - Values: -1.0 to 1.0 (normalized)

    Example:
        >>> pcm_bytes = b'\\x00\\x00\\x00\\x40\\x00\\xc0\\xff\\x7f\\x00\\x80'
        >>> audio = pcm16_to_float32(pcm_bytes)
        >>> audio.shape
        (5,)
    """
    # Convert bytes to int16 array
    audio_int16 = np.frombuffer(pcm_bytes, dtype=np.int16)

    # Normalize to [-1.0, 1.0]
    audio_float = audio_int16.astype(np.float32) / 32768.0

    # Reshape for multi-channel if needed
    if num_channels > 1:
        num_samples = len(audio_float) // num_channels
        audio_float = audio_float.reshape(num_samples, num_channels)

    return audio_float


def prepare_for_gemini(stereo_audio: np.ndarray) -> Tuple[bytes, str]:
    """
    Prepare robot audio for sending to Gemini Live API.

    Converts stereo 16kHz audio to mono 16kHz PCM bytes.

    Args:
        stereo_audio: Robot audio (stereo, 16kHz)
            - Shape: (num_samples, 2)
            - dtype: float32
            - Values: -1.0 to 1.0

    Returns:
        Tuple of (pcm_bytes, mime_type):
            - pcm_bytes: Raw 16-bit PCM audio bytes
            - mime_type: "audio/pcm;rate=16000"

    Example:
        >>> robot_audio = np.random.randn(1600, 2).astype(np.float32) * 0.1
        >>> pcm_bytes, mime_type = prepare_for_gemini(robot_audio)
        >>> mime_type
        'audio/pcm;rate=16000'
    """
    # Step 1: Convert stereo to mono
    mono_audio = stereo_to_mono(stereo_audio)

    # Step 2: Convert to 16-bit PCM bytes
    pcm_bytes = float32_to_pcm16(mono_audio)

    return pcm_bytes, "audio/pcm;rate=16000"


def prepare_from_gemini(
    pcm_bytes: bytes, sample_rate: int = 24000
) -> np.ndarray:
    """
    Prepare Gemini audio for playing on robot speakers.

    Converts mono PCM bytes (typically 24kHz) to stereo 16kHz float32.

    Args:
        pcm_bytes: Raw 16-bit PCM audio bytes from Gemini
        sample_rate: Sample rate of the incoming audio (24000 or 16000)

    Returns:
        Robot-compatible audio (stereo, 16kHz)
            - Shape: (num_samples, 2)
            - dtype: float32
            - Values: -1.0 to 1.0

    Example:
        >>> pcm_bytes = (np.random.randn(2400) * 1000).astype(np.int16).tobytes()
        >>> robot_audio = prepare_from_gemini(pcm_bytes, sample_rate=24000)
        >>> robot_audio.shape[1]
        2  # Stereo
    """
    # Step 1: Convert PCM bytes to float32 mono
    mono_audio = pcm16_to_float32(pcm_bytes, num_channels=1)

    # Step 2: Resample if needed (24kHz -> 16kHz)
    if sample_rate == 24000:
        mono_audio = resample_24k_to_16k(mono_audio)
    elif sample_rate != 16000:
        raise ValueError(f"Unsupported sample rate: {sample_rate}")

    # Step 3: Convert mono to stereo
    stereo_audio = mono_to_stereo(mono_audio)

    return stereo_audio


# Convenience function for getting audio info
def get_audio_info(audio: np.ndarray) -> dict:
    """
    Get information about an audio array.

    Args:
        audio: Audio array (any shape)

    Returns:
        Dictionary with audio information:
            - shape: Array shape
            - dtype: Data type
            - duration_seconds: Duration in seconds (assuming 16kHz)
            - num_channels: Number of channels (1 for mono, 2 for stereo)
            - min_value: Minimum value
            - max_value: Maximum value
            - mean_amplitude: Mean absolute amplitude

    Example:
        >>> audio = np.random.randn(16000, 2).astype(np.float32) * 0.1
        >>> info = get_audio_info(audio)
        >>> info['duration_seconds']
        1.0
    """
    num_samples = audio.shape[0] if audio.ndim >= 1 else 0
    num_channels = audio.shape[1] if audio.ndim == 2 else 1

    return {
        "shape": audio.shape,
        "dtype": audio.dtype,
        "duration_seconds": num_samples / 16000,
        "num_channels": num_channels,
        "min_value": float(audio.min()),
        "max_value": float(audio.max()),
        "mean_amplitude": float(np.abs(audio).mean()),
    }

"""
Unit tests for audio converter utilities.

Tests all audio format conversions needed for Reachy Mini ↔ Gemini integration.
"""

import pytest
import numpy as np
from reachy_mini_companion.audio_converters import (
    stereo_to_mono,
    mono_to_stereo,
    resample_24k_to_16k,
    float32_to_pcm16,
    pcm16_to_float32,
    prepare_for_gemini,
    prepare_from_gemini,
    get_audio_info,
)


class TestStereoToMono:
    """Tests for stereo_to_mono function."""

    def test_basic_conversion(self):
        """Test basic stereo to mono conversion."""
        # Create stereo audio: [[L, R], [L, R], ...]
        stereo = np.array([[0.5, 0.3], [0.2, 0.4], [-0.1, 0.1]], dtype=np.float32)

        mono = stereo_to_mono(stereo)

        # Check shape
        assert mono.shape == (3,)
        assert mono.ndim == 1

        # Check values (should be average of L and R)
        assert np.isclose(mono[0], 0.4)  # (0.5 + 0.3) / 2
        assert np.isclose(mono[1], 0.3)  # (0.2 + 0.4) / 2
        assert np.isclose(mono[2], 0.0)  # (-0.1 + 0.1) / 2

    def test_large_audio(self):
        """Test with realistic audio chunk size (1 second at 16kHz)."""
        stereo = np.random.randn(16000, 2).astype(np.float32) * 0.5

        mono = stereo_to_mono(stereo)

        assert mono.shape == (16000,)
        assert mono.dtype == np.float32
        # Mono should have similar amplitude range as stereo
        assert np.abs(mono).max() <= np.abs(stereo).max()

    def test_silent_audio(self):
        """Test with silent audio (all zeros)."""
        stereo = np.zeros((100, 2), dtype=np.float32)

        mono = stereo_to_mono(stereo)

        assert mono.shape == (100,)
        assert np.allclose(mono, 0.0)

    def test_invalid_shape(self):
        """Test that invalid shapes raise ValueError."""
        # Test with 1D array (not stereo)
        with pytest.raises(ValueError, match="Expected stereo audio"):
            stereo_to_mono(np.array([1, 2, 3]))

        # Test with 3 channels (not stereo)
        with pytest.raises(ValueError, match="Expected stereo audio"):
            stereo_to_mono(np.array([[1, 2, 3], [4, 5, 6]]))


class TestMonoToStereo:
    """Tests for mono_to_stereo function."""

    def test_basic_conversion(self):
        """Test basic mono to stereo conversion."""
        mono = np.array([0.5, 0.2, -0.1], dtype=np.float32)

        stereo = mono_to_stereo(mono)

        # Check shape
        assert stereo.shape == (3, 2)
        assert stereo.ndim == 2

        # Check values (both channels should be identical)
        assert np.allclose(stereo[:, 0], mono)  # Left channel
        assert np.allclose(stereo[:, 1], mono)  # Right channel

    def test_large_audio(self):
        """Test with realistic audio chunk size (1 second at 16kHz)."""
        mono = np.random.randn(16000).astype(np.float32) * 0.5

        stereo = mono_to_stereo(mono)

        assert stereo.shape == (16000, 2)
        assert stereo.dtype == np.float32
        # Both channels should be identical
        assert np.allclose(stereo[:, 0], stereo[:, 1])

    def test_silent_audio(self):
        """Test with silent audio (all zeros)."""
        mono = np.zeros(100, dtype=np.float32)

        stereo = mono_to_stereo(mono)

        assert stereo.shape == (100, 2)
        assert np.allclose(stereo, 0.0)

    def test_invalid_shape(self):
        """Test that invalid shapes raise ValueError."""
        # Test with 2D array (not mono)
        with pytest.raises(ValueError, match="Expected mono audio"):
            mono_to_stereo(np.array([[1, 2], [3, 4]]))


class TestRoundTrip:
    """Test stereo -> mono -> stereo conversions."""

    def test_stereo_to_mono_to_stereo(self):
        """Test that stereo -> mono -> stereo preserves mono content."""
        # Create stereo with identical channels
        mono_orig = np.array([0.5, 0.2, -0.1], dtype=np.float32)
        stereo_orig = mono_to_stereo(mono_orig)

        # Convert to mono and back
        mono = stereo_to_mono(stereo_orig)
        stereo_reconstructed = mono_to_stereo(mono)

        # Should match original
        assert np.allclose(stereo_reconstructed, stereo_orig)

    def test_mono_to_stereo_to_mono(self):
        """Test that mono -> stereo -> mono preserves audio."""
        mono_orig = np.array([0.5, 0.2, -0.1], dtype=np.float32)

        # Convert to stereo and back
        stereo = mono_to_stereo(mono_orig)
        mono_reconstructed = stereo_to_mono(stereo)

        # Should match original
        assert np.allclose(mono_reconstructed, mono_orig)


class TestResample24kTo16k:
    """Tests for resample_24k_to_16k function."""

    def test_basic_resampling(self):
        """Test basic 24kHz to 16kHz resampling."""
        # Create 1 second of 440Hz sine wave at 24kHz
        duration = 1.0
        sample_rate_24k = 24000
        frequency = 440.0

        t = np.arange(int(duration * sample_rate_24k)) / sample_rate_24k
        audio_24k = np.sin(2 * np.pi * frequency * t).astype(np.float32)

        # Resample to 16kHz
        audio_16k = resample_24k_to_16k(audio_24k)

        # Check length (should be 2/3 of original)
        expected_length = len(audio_24k) * 2 // 3
        assert len(audio_16k) == expected_length
        assert audio_16k.dtype == np.float32

    def test_resampling_preserves_amplitude(self):
        """Test that resampling preserves amplitude range."""
        # Create audio with known amplitude
        audio_24k = np.random.randn(24000).astype(np.float32) * 0.5

        audio_16k = resample_24k_to_16k(audio_24k)

        # Resampling can introduce small overshoot due to interpolation
        # Allow up to 2x the input range (this is normal for signal processing)
        assert np.abs(audio_16k).max() <= 2.0
        # Mean amplitude should be similar (within 20%)
        amp_24k = np.abs(audio_24k).mean()
        amp_16k = np.abs(audio_16k).mean()
        assert 0.8 * amp_24k < amp_16k < 1.2 * amp_24k

    def test_short_audio(self):
        """Test resampling with short audio chunks."""
        # 100ms at 24kHz = 2400 samples
        audio_24k = np.random.randn(2400).astype(np.float32) * 0.3

        audio_16k = resample_24k_to_16k(audio_24k)

        # Should be ~1600 samples (100ms at 16kHz)
        assert len(audio_16k) == 1600

    def test_invalid_shape(self):
        """Test that invalid shapes raise ValueError."""
        # Test with 2D array (not mono)
        with pytest.raises(ValueError, match="Expected mono audio"):
            resample_24k_to_16k(np.array([[1, 2], [3, 4]]))


class TestFloat32ToPcm16:
    """Tests for float32_to_pcm16 function."""

    def test_basic_conversion(self):
        """Test basic float32 to PCM16 conversion."""
        audio = np.array([0.0, 0.5, -0.5, 1.0, -1.0], dtype=np.float32)

        pcm_bytes = float32_to_pcm16(audio)

        # Check type and length
        assert isinstance(pcm_bytes, bytes)
        assert len(pcm_bytes) == len(audio) * 2  # 2 bytes per sample

    def test_value_range(self):
        """Test that values are properly scaled to int16 range."""
        # Test extreme values
        audio = np.array([-1.0, 0.0, 1.0], dtype=np.float32)

        pcm_bytes = float32_to_pcm16(audio)

        # Convert back to verify
        pcm_int16 = np.frombuffer(pcm_bytes, dtype=np.int16)
        assert pcm_int16[0] == -32767  # -1.0 -> -32767
        assert pcm_int16[1] == 0  # 0.0 -> 0
        assert pcm_int16[2] == 32767  # 1.0 -> 32767

    def test_clipping(self):
        """Test that values outside [-1, 1] are clipped."""
        # Create audio with values outside valid range
        audio = np.array([-2.0, 1.5, 0.5], dtype=np.float32)

        pcm_bytes = float32_to_pcm16(audio)

        # Convert back to verify clipping
        pcm_int16 = np.frombuffer(pcm_bytes, dtype=np.int16)
        assert pcm_int16[0] == -32767  # -2.0 clipped to -1.0
        assert pcm_int16[1] == 32767  # 1.5 clipped to 1.0
        assert -32767 <= pcm_int16[2] <= 32767  # 0.5 within range


class TestPcm16ToFloat32:
    """Tests for pcm16_to_float32 function."""

    def test_basic_conversion(self):
        """Test basic PCM16 to float32 conversion."""
        # Create int16 PCM data
        pcm_int16 = np.array([0, 16384, -16384, 32767, -32768], dtype=np.int16)
        pcm_bytes = pcm_int16.tobytes()

        audio = pcm16_to_float32(pcm_bytes)

        # Check shape and type
        assert audio.shape == (5,)
        assert audio.dtype == np.float32

        # Check normalization
        assert -1.0 <= audio.min() <= 1.0
        assert -1.0 <= audio.max() <= 1.0

    def test_value_range(self):
        """Test that int16 values are properly normalized."""
        # Test extreme values
        pcm_int16 = np.array([-32768, 0, 32767], dtype=np.int16)
        pcm_bytes = pcm_int16.tobytes()

        audio = pcm16_to_float32(pcm_bytes)

        assert np.isclose(audio[0], -1.0, atol=0.01)  # -32768 -> -1.0
        assert audio[1] == 0.0  # 0 -> 0.0
        assert np.isclose(audio[2], 1.0, atol=0.01)  # 32767 -> ~1.0

    def test_stereo_conversion(self):
        """Test conversion with stereo audio."""
        # Create stereo PCM data (LRLRLR...)
        pcm_int16 = np.array([100, 200, 300, 400, 500, 600], dtype=np.int16)
        pcm_bytes = pcm_int16.tobytes()

        audio = pcm16_to_float32(pcm_bytes, num_channels=2)

        # Check shape (should be reshaped to (samples, 2))
        assert audio.shape == (3, 2)
        assert audio.dtype == np.float32


class TestRoundTripPcmConversion:
    """Test float32 -> PCM16 -> float32 conversions."""

    def test_round_trip_conversion(self):
        """Test that float32 -> PCM16 -> float32 preserves audio."""
        # Create random audio within valid range [-1.0, 1.0]
        # Use uniform distribution to ensure values stay within range
        audio_orig = (np.random.rand(1000).astype(np.float32) - 0.5) * 2 * 0.9  # Scale to [-0.9, 0.9]

        # Convert to PCM and back
        pcm_bytes = float32_to_pcm16(audio_orig)
        audio_reconstructed = pcm16_to_float32(pcm_bytes)

        # 16-bit PCM has resolution of 1/32768 ≈ 3e-5
        # Allow tolerance for quantization error (about 3x PCM resolution)
        assert np.allclose(audio_reconstructed, audio_orig, atol=1e-4)


class TestPrepareForGemini:
    """Tests for prepare_for_gemini function."""

    def test_basic_preparation(self):
        """Test preparing robot audio for Gemini."""
        # Create stereo robot audio (16kHz)
        robot_audio = np.random.randn(1600, 2).astype(np.float32) * 0.3

        pcm_bytes, mime_type = prepare_for_gemini(robot_audio)

        # Check outputs
        assert isinstance(pcm_bytes, bytes)
        assert mime_type == "audio/pcm;rate=16000"
        # Should have converted stereo to mono (half the samples)
        assert len(pcm_bytes) == 1600 * 2  # 1600 samples * 2 bytes per sample

    def test_realistic_chunk(self):
        """Test with realistic audio chunk (100ms)."""
        # 100ms at 16kHz = 1600 samples
        robot_audio = np.random.randn(1600, 2).astype(np.float32) * 0.1

        pcm_bytes, mime_type = prepare_for_gemini(robot_audio)

        assert len(pcm_bytes) == 1600 * 2  # Mono: 1600 samples * 2 bytes


class TestPrepareFromGemini:
    """Tests for prepare_from_gemini function."""

    def test_basic_preparation_24k(self):
        """Test preparing Gemini audio (24kHz) for robot."""
        # Create mono PCM audio at 24kHz (1 second)
        audio_24k = (np.random.randn(24000) * 5000).astype(np.int16)
        pcm_bytes = audio_24k.tobytes()

        robot_audio = prepare_from_gemini(pcm_bytes, sample_rate=24000)

        # Check shape: should be stereo at 16kHz
        assert robot_audio.shape[1] == 2  # Stereo
        assert robot_audio.shape[0] == 16000  # Resampled to 16kHz
        assert robot_audio.dtype == np.float32

    def test_basic_preparation_16k(self):
        """Test preparing Gemini audio (16kHz) for robot."""
        # Create mono PCM audio at 16kHz (1 second)
        audio_16k = (np.random.randn(16000) * 5000).astype(np.int16)
        pcm_bytes = audio_16k.tobytes()

        robot_audio = prepare_from_gemini(pcm_bytes, sample_rate=16000)

        # Check shape: should be stereo at 16kHz (no resampling)
        assert robot_audio.shape[1] == 2  # Stereo
        assert robot_audio.shape[0] == 16000  # Same length
        assert robot_audio.dtype == np.float32

    def test_invalid_sample_rate(self):
        """Test that invalid sample rates raise ValueError."""
        pcm_bytes = np.zeros(100, dtype=np.int16).tobytes()

        with pytest.raises(ValueError, match="Unsupported sample rate"):
            prepare_from_gemini(pcm_bytes, sample_rate=48000)


class TestGetAudioInfo:
    """Tests for get_audio_info function."""

    def test_mono_audio_info(self):
        """Test getting info for mono audio."""
        audio = np.random.randn(16000).astype(np.float32) * 0.5

        info = get_audio_info(audio)

        assert info["shape"] == (16000,)
        assert info["dtype"] == np.float32
        assert info["duration_seconds"] == 1.0  # 16000 samples / 16000 Hz
        assert info["num_channels"] == 1
        assert "min_value" in info
        assert "max_value" in info
        assert "mean_amplitude" in info

    def test_stereo_audio_info(self):
        """Test getting info for stereo audio."""
        audio = np.random.randn(16000, 2).astype(np.float32) * 0.5

        info = get_audio_info(audio)

        assert info["shape"] == (16000, 2)
        assert info["dtype"] == np.float32
        assert info["duration_seconds"] == 1.0
        assert info["num_channels"] == 2

    def test_short_audio_info(self):
        """Test getting info for short audio (100ms)."""
        audio = np.random.randn(1600, 2).astype(np.float32) * 0.3

        info = get_audio_info(audio)

        assert info["duration_seconds"] == 0.1  # 1600 samples / 16000 Hz


class TestEndToEndIntegration:
    """Integration tests for complete audio pipeline."""

    def test_robot_to_gemini_to_robot(self):
        """Test complete pipeline: Robot -> Gemini -> Robot."""
        # 1. Start with robot audio (stereo, 16kHz)
        robot_audio_in = np.random.randn(1600, 2).astype(np.float32) * 0.3

        # 2. Prepare for Gemini (stereo -> mono PCM)
        pcm_bytes_to_gemini, mime_type = prepare_for_gemini(robot_audio_in)

        # 3. Simulate Gemini response (mono PCM at 24kHz)
        # In reality, this comes from Gemini API
        # For testing, we'll just use the same audio upsampled
        simulated_gemini_response = (
            np.random.randn(2400) * 5000
        ).astype(np.int16).tobytes()

        # 4. Prepare from Gemini (mono PCM -> stereo 16kHz)
        robot_audio_out = prepare_from_gemini(
            simulated_gemini_response, sample_rate=24000
        )

        # 5. Verify output format
        assert robot_audio_out.shape[1] == 2  # Stereo
        assert robot_audio_out.dtype == np.float32
        assert -1.0 <= robot_audio_out.min() <= 1.0
        assert -1.0 <= robot_audio_out.max() <= 1.0

    def test_realistic_conversation_chunk(self):
        """Test with realistic conversation chunk (100ms)."""
        # Robot records 100ms chunk (1600 samples at 16kHz)
        robot_chunk = np.random.randn(1600, 2).astype(np.float32) * 0.2

        # Send to Gemini
        pcm_bytes, _ = prepare_for_gemini(robot_chunk)

        # Simulate Gemini response (100ms at 24kHz = 2400 samples)
        gemini_response = (np.random.randn(2400) * 3000).astype(np.int16).tobytes()

        # Receive from Gemini
        robot_output = prepare_from_gemini(gemini_response, sample_rate=24000)

        # Should be playable on robot
        assert robot_output.shape == (1600, 2)
        assert robot_output.dtype == np.float32

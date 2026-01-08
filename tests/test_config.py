"""
Unit tests for configuration loading.

Tests the Config class and environment variable handling.
"""

import os
import pytest
from pathlib import Path


def test_config_module_imports():
    """Test that config module can be imported."""
    from reachy_mini_companion import config
    assert config is not None


def test_config_has_required_attributes():
    """Test that config has all required attributes."""
    from reachy_mini_companion.config import config

    if config is None:
        pytest.skip("Config not loaded (missing .env file)")

    assert hasattr(config, 'GEMINI_API_KEY')
    assert hasattr(config, 'GEMINI_MODEL')
    assert hasattr(config, 'VERBOSE')
    assert hasattr(config, 'ENV_PATH')


def test_config_api_key_format():
    """Test that API key has expected format (if loaded)."""
    from reachy_mini_companion.config import config

    if config is None:
        pytest.skip("Config not loaded (missing .env file)")

    # API key should be a non-empty string
    assert isinstance(config.GEMINI_API_KEY, str)
    assert len(config.GEMINI_API_KEY) > 0

    # Google API keys typically start with specific patterns
    # This is a loose check - just ensuring it's not obviously wrong
    assert len(config.GEMINI_API_KEY) > 20, "API key seems too short"


def test_config_model_is_set():
    """Test that model name is properly set."""
    from reachy_mini_companion.config import config

    if config is None:
        pytest.skip("Config not loaded (missing .env file)")

    assert isinstance(config.GEMINI_MODEL, str)
    assert len(config.GEMINI_MODEL) > 0
    # Should contain "gemini" somewhere
    assert "gemini" in config.GEMINI_MODEL.lower()


def test_config_verbose_is_boolean():
    """Test that verbose setting is a boolean."""
    from reachy_mini_companion.config import config

    if config is None:
        pytest.skip("Config not loaded (missing .env file)")

    assert isinstance(config.VERBOSE, bool)


def test_config_env_path_exists():
    """Test that .env file path is valid."""
    from reachy_mini_companion.config import config

    if config is None:
        pytest.skip("Config not loaded (missing .env file)")

    assert isinstance(config.ENV_PATH, Path)
    # If config loaded successfully, the .env file should exist
    assert config.ENV_PATH.exists(), f".env file not found at {config.ENV_PATH}"


def test_config_repr_hides_api_key():
    """Test that config representation doesn't expose full API key."""
    from reachy_mini_companion.config import config

    if config is None:
        pytest.skip("Config not loaded (missing .env file)")

    repr_str = repr(config)

    # Should contain "***" to indicate hidden key
    assert "***" in repr_str

    # Should NOT contain the full API key
    if config.GEMINI_API_KEY and len(config.GEMINI_API_KEY) > 4:
        # Check that the beginning of the API key is not in the repr
        key_start = config.GEMINI_API_KEY[:10]
        assert key_start not in repr_str, "Full API key exposed in repr!"

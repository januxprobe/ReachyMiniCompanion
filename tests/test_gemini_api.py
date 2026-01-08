"""
Integration tests for Gemini API connection.

These tests make actual API calls and require a valid GEMINI_API_KEY.
Mark as slow/integration tests that can be skipped in CI.
"""

import pytest
from google import genai


@pytest.fixture
def gemini_client():
    """Fixture to create a Gemini client for testing."""
    from reachy_mini_companion.config import config

    if config is None:
        pytest.skip("Config not loaded (missing .env file)")

    client = genai.Client(api_key=config.GEMINI_API_KEY)
    return client


@pytest.fixture
def gemini_model():
    """Fixture to get the configured Gemini model name."""
    from reachy_mini_companion.config import config

    if config is None:
        pytest.skip("Config not loaded (missing .env file)")

    return config.GEMINI_MODEL


@pytest.mark.integration
@pytest.mark.slow
def test_gemini_client_creation(gemini_client):
    """Test that Gemini client can be created."""
    assert gemini_client is not None


@pytest.mark.integration
@pytest.mark.slow
def test_gemini_simple_generation(gemini_client, gemini_model):
    """Test simple text generation with Gemini."""
    response = gemini_client.models.generate_content(
        model=gemini_model,
        contents="Say hello in one sentence"
    )

    # Should get a response
    assert response is not None
    assert hasattr(response, 'text')

    # Response should be a non-empty string
    assert isinstance(response.text, str)
    assert len(response.text) > 0

    # Response should be somewhat reasonable (contains greeting words)
    text_lower = response.text.lower()
    greeting_words = ['hello', 'hi', 'hey', 'greetings']
    assert any(word in text_lower for word in greeting_words), \
        f"Expected greeting, got: {response.text}"


@pytest.mark.integration
@pytest.mark.slow
def test_gemini_with_context(gemini_client, gemini_model):
    """Test Gemini generation with robot context."""
    prompt = """You are a friendly desk companion robot named Reachy Mini.
    Introduce yourself in one fun sentence!"""

    response = gemini_client.models.generate_content(
        model=gemini_model,
        contents=prompt
    )

    assert response is not None
    text = response.text

    # Should mention Reachy Mini (though model might vary capitalization)
    assert 'reachy' in text.lower(), \
        f"Expected 'Reachy' in response, got: {text}"


@pytest.mark.integration
@pytest.mark.slow
def test_gemini_response_format(gemini_client, gemini_model):
    """Test that Gemini response has expected attributes."""
    response = gemini_client.models.generate_content(
        model=gemini_model,
        contents="Test"
    )

    # Check response structure
    assert hasattr(response, 'text')

    # Text should be a string
    assert isinstance(response.text, str)


@pytest.mark.integration
@pytest.mark.slow
def test_gemini_multiple_calls(gemini_client, gemini_model):
    """Test that multiple API calls work."""
    prompts = [
        "Say hi",
        "Count to 3",
        "What's 2+2?"
    ]

    for prompt in prompts:
        response = gemini_client.models.generate_content(
            model=gemini_model,
            contents=prompt
        )
        assert response is not None
        assert len(response.text) > 0

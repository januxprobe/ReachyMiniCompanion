"""
Configuration Management for Reachy Mini Companion

This module safely loads configuration from environment variables.
API keys are stored in a .env file (git-ignored) for security.

How it works:
1. load_dotenv() reads the .env file
2. os.getenv() retrieves environment variables
3. If a key is missing, we provide helpful error messages
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Find the .env file (should be in the project root)
# __file__ is this config.py file
# .parent gets the reachy_mini_companion directory
# .parent again gets the project root
project_root = Path(__file__).parent.parent
env_path = project_root / ".env"

# Load environment variables from .env file
# If .env doesn't exist, this doesn't crash - it just does nothing
load_dotenv(dotenv_path=env_path)


class Config:
    """
    Configuration settings loaded from environment variables.

    Access settings like:
        from reachy_mini_companion.config import config
        api_key = config.GEMINI_API_KEY
    """

    def __init__(self):
        """Load all configuration from environment variables."""

        # Gemini API Key (required)
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        if not self.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY not found in environment variables.\n"
                "Please create a .env file from .env.example and add your API key.\n"
                "Get your key at: https://aistudio.google.com/app/apikey"
            )

        # Gemini model to use (optional, has default)
        self.GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")

        # Verbose logging (optional, has default)
        verbose_str = os.getenv("VERBOSE", "true")
        self.VERBOSE = verbose_str.lower() in ("true", "1", "yes")

        # Path to .env file (for debugging)
        self.ENV_PATH = env_path

    def __repr__(self):
        """String representation (hides API key for security)."""
        key_preview = "***" + self.GEMINI_API_KEY[-4:] if self.GEMINI_API_KEY else "NOT SET"
        return (
            f"Config(\n"
            f"  GEMINI_API_KEY={key_preview},\n"
            f"  GEMINI_MODEL={self.GEMINI_MODEL},\n"
            f"  VERBOSE={self.VERBOSE},\n"
            f"  ENV_PATH={self.ENV_PATH}\n"
            f")"
        )


# Create a singleton instance that can be imported
# Usage: from reachy_mini_companion.config import config
try:
    config = Config()
except ValueError as e:
    # If API key is missing, we still create a config object
    # but with a clear error message
    print(f"⚠️  Configuration Error: {e}")
    config = None


# Example usage (for testing this file directly)
if __name__ == "__main__":
    print("=" * 60)
    print("Reachy Mini Companion - Configuration")
    print("=" * 60)

    if config:
        print("\n✅ Configuration loaded successfully!")
        print(config)
        print("\n💡 Your API key is loaded and ready to use.")
        print("   (Only the last 4 characters are shown for security)")
    else:
        print("\n❌ Configuration failed to load.")
        print("   Please check the error message above.")

    print("\n" + "=" * 60)

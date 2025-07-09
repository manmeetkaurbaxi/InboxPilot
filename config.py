"""
Configuration settings for the CV Extractor application
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SENDER_NAME = os.getenv("SENDER_NAME", "Your Name")

# Model Configuration
GROQ_MODEL = "groq:llama-3.3-70b-versatile"  # Currently supported model

# Available Groq Models (for reference)
AVAILABLE_GROQ_MODELS = {
    "llama-3.3-70b-versatile": "High performance, versatile model",
    "llama-3.1-8b-instant": "Fast, lightweight model",
    "mixtral-8x7b-32768": "Mixtral model with large context",
    "gemma-7b-it": "Google's Gemma model"
}

# Application Settings
MAX_FILE_SIZE_MB = 10
SUPPORTED_FILE_TYPES = ['pdf']
DEFAULT_TEMPERATURE = 0.1  # Low temperature for consistent extraction

def validate_config():
    """Validate that required configuration is present"""
    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY not found in environment variables. "
            "Please set it in your .env file or run python setup_env.py"
        )
    return True

def get_model_info():
    """Get information about the current model"""
    return {
        "model": GROQ_MODEL,
        "description": AVAILABLE_GROQ_MODELS.get(GROQ_MODEL, "Unknown model"),
        "available_models": AVAILABLE_GROQ_MODELS
    } 
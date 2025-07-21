"""Configuration settings for Twelve Labs API."""

import os
from typing import Optional

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for Twelve Labs API."""
    
    # API Configuration
    API_KEY: str = os.getenv("TWELVE_LABS_API_KEY", "tlk_2TW8RSN1DK2JH220EPXZH39WPBVW")
    BASE_URL: str = "https://api.twelvelabs.io/v1.3"
    
    # Default settings
    DEFAULT_MODEL: str = "embed-english-v1"
    DEFAULT_INDEX_ID: str = "existing_assets"
    
    # Processing settings
    MAX_RETRIES: int = 3
    RETRY_DELAY: float = 1.0
    
    # Modalities
    MODALITIES = {
        "video": "video",
        "audio": "audio", 
        "text": "text",
        "image": "image"
    }
    
    # Available models
    MODELS = {
        "embed": ["embed-english-v1", "embed-multilingual-v1"],
        "generate": ["generate-english-v1", "generate-multilingual-v1"],
        "search": ["search-english-v1", "search-multilingual-v1"]
    }
    
    @classmethod
    def get_api_key(cls) -> str:
        """Get the API key."""
        return cls.API_KEY
    
    @classmethod
    def validate_api_key(cls) -> bool:
        """Validate that API key is set."""
        return bool(cls.API_KEY and cls.API_KEY.startswith("tlk_")) 
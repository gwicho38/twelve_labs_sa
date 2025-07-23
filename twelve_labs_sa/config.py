"""Configuration settings for Twelve Labs API."""

import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for Twelve Labs API."""
    
    # API Configuration
    API_KEY: str = os.getenv("TWELVE_LABS_API_KEY", "")
    BASE_URL: str = "https://api.twelvelabs.io/v1.3"
    
    # Storage Configuration - LanceDB is now the default
    USE_LANCEDB: bool = os.getenv("TWELVE_LABS_USE_LANCEDB", "true").lower() == "true"
    
    # Default settings
    DEFAULT_MODEL: str = "marengo2.7"
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
        "embed": ["Marengo-retrieval-2.6"],
        "generate": ["pegasus1.2"],
        "search": ["marengo2.7"]
    }
    
    @classmethod
    def get_api_key(cls) -> str:
        """Get the API key."""
        if not cls.API_KEY:
            raise ValueError("TWELVE_LABS_API_KEY environment variable is not set. Please set your API key.")
        return cls.API_KEY
    
    @classmethod
    def validate_api_key(cls) -> bool:
        """Validate that API key is set."""
        return bool(cls.API_KEY and cls.API_KEY.startswith("tlk_"))
    
    @classmethod
    def use_lancedb(cls) -> bool:
        """Check if LanceDB should be used as the default storage backend."""
        return cls.USE_LANCEDB
    
    @classmethod
    def set_use_lancedb(cls, enabled: bool) -> None:
        """Set whether to use LanceDB as the default storage backend."""
        cls.USE_LANCEDB = enabled 
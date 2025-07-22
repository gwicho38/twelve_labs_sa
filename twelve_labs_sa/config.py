"""Configuration settings for Twelve Labs API."""

import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for Twelve Labs API."""
    
    # API Configuration
    API_KEY: str = os.getenv("TWELVE_LABS_API_KEY", "tlk_2TW8RSN1DK2JH220EPXZH39WPBVW")
    BASE_URL: str = "https://api.twelvelabs.io/v1.3"
    
    # Simulation mode - set to True for simulated API calls, False for real API calls
    SIMULATION_MODE: bool = os.getenv("TWELVE_LABS_SIMULATION_MODE", "true").lower() == "true"
    
    # Storage Configuration - LanceDB is now the default
    USE_LANCEDB: bool = os.getenv("TWELVE_LABS_USE_LANCEDB", "true").lower() == "true"
    
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
    
    @classmethod
    def is_simulation_mode(cls) -> bool:
        """Check if simulation mode is enabled."""
        return cls.SIMULATION_MODE
    
    @classmethod
    def set_simulation_mode(cls, enabled: bool) -> None:
        """Set simulation mode."""
        cls.SIMULATION_MODE = enabled
    
    @classmethod
    def use_lancedb(cls) -> bool:
        """Check if LanceDB should be used as the default storage backend."""
        return cls.USE_LANCEDB
    
    @classmethod
    def set_use_lancedb(cls, enabled: bool) -> None:
        """Set whether to use LanceDB as the default storage backend."""
        cls.USE_LANCEDB = enabled 
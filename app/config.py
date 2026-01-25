"""
Application Configuration

Loads environment variables and provides settings to the application.
Uses Pydantic Settings for type-safe configuration management.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Attributes:
        DATABASE_URL: Connection string for the database
        SECRET_KEY: Secret key for JWT token signing
        ALGORITHM: Algorithm used for JWT encoding
        ACCESS_TOKEN_EXPIRE_MINUTES: Token expiration time in minutes
        DEBUG: Enable debug mode
        APP_NAME: Application name shown in docs
        APP_VERSION: Current API version
    """
    
    # Database settings
    DATABASE_URL: str = "sqlite:///./ecommerce.db"
    
    # JWT settings
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Application settings
    DEBUG: bool = True
    APP_NAME: str = "E-commerce API"
    APP_VERSION: str = "1.0.0"
    
    class Config:
        # Load from .env file if it exists
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Using lru_cache ensures settings are loaded only once.
    """
    return Settings()


# Global settings instance
settings = get_settings()

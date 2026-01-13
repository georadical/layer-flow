from dotenv import load_dotenv
import os
from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache

# Explicitly load .env to ensure it's picked up even if Pydantic misses it
load_dotenv()

class Settings(BaseSettings):
    """
    Application configuration settings.
    Values are read from environment variables or defaults.
    """
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "layer-flow"
    DEBUG: bool = True
    
    # Database settings
    DATABASE_URL: str
    
    ENVIRONMENT: str = "local"
    
    # Auth settings
    SECRET_KEY: str = "supersecretkey" # Change in production!
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Session Settings (for OAuth state)
    SESSION_SECRET_KEY: str = "super-secret-session-key"

    # Google OAuth Settings
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/google/callback"

    # Microsoft OAuth Settings
    MICROSOFT_CLIENT_ID: str = ""
    MICROSOFT_CLIENT_SECRET: str = ""
    MICROSOFT_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/microsoft/callback"

    # GitHub OAuth Settings
    GITHUB_CLIENT_ID: str = ""
    GITHUB_CLIENT_SECRET: str = ""
    GITHUB_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/github/callback"

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """
    Returns a cached instance of the Settings class.
    """
    return Settings()

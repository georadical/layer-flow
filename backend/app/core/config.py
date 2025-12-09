from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache

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

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """
    Returns a cached instance of the Settings class.
    """
    return Settings()

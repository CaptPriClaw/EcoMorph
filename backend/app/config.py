# backend/app/config.py

from pydantic import BaseSettings

class Settings(BaseSettings):
    # Database URL
    DATABASE_URL: str = "sqlite:///./ecomorph.db" # Default to SQLite for easy setup

    # JWT Settings from auth_service
    SECRET_KEY: str = "your-super-secret-key-that-is-long-and-random"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        # This tells pydantic to read from a .env file
        env_file = ".env"

# Create a single instance of the settings to be imported elsewhere
settings = Settings()
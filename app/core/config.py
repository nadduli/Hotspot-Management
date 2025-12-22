#!/usr/bin/python3
"""App Configuration"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """
    Docstring for Settings
    """

    APP_NAME: str = "Hotspot Management"
    DEBUG: bool = False
    LOG_LEVEL: str

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

@lru_cache()
def get_settings() -> Settings:
    """Get Settings"""
    return Settings()

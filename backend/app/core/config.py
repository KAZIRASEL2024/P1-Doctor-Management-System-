"""Application configuration using pydantic-settings."""
from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Application
    APP_NAME: str = "Human Doctor Management System"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = (
        "postgresql+psycopg://dms_user:change_me_in_production@localhost:5432/doctor_management"
    )

    # Security
    SECRET_KEY: str = "dev_secret_key_change_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # CORS
    BACKEND_CORS_ORIGINS: str = "http://localhost:3000"

    # Demo data
    SEED_DEMO_DATA: bool = False
    ADMIN_EMAIL: str | None = None
    ADMIN_PASSWORD: str | None = None

    # SLA settings (minutes)
    SLA_NORMAL_MINUTES: int = 480   # 8 hours
    SLA_URGENT_MINUTES: int = 120   # 2 hours
    SLA_EMERGENCY_MINUTES: int = 30 # 30 minutes

    # Operating hours (24h format, UTC+6 Bangladesh time)
    OPERATING_HOUR_START: int = 8   # 8:00 AM
    OPERATING_HOUR_END: int = 20    # 8:00 PM

    @property
    def cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.BACKEND_CORS_ORIGINS.split(",")]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

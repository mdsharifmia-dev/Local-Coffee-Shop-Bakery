import os
from typing import List, Union
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    APP_NAME: str = "Local Coffee Shop & Bakery"
    APP_ENV: str = Field(default="development", description="development | staging | production")
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database Configuration (SQLite default for zero-setup local run; PostgreSQL in production)
    DATABASE_URL: str = "sqlite+aiosqlite:///./coffee_shop.db"
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30

    # Redis Cache & Rate Limiting
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_TTL_SECONDS: int = 300
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 60

    # CORS & Security
    ALLOWED_ORIGINS: Union[List[str], str] = ["*"]
    ADMIN_API_KEY: str = "dev-admin-secret-key-change-in-production"

    # Business & Notification Settings
    WHATSAPP_NUMBER: str = "8801700000000"
    NOTIFICATION_EMAIL_TO: str = "orders@localcoffeeshop.com"
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""


settings = Settings()

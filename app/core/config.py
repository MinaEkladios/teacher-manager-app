"""
TeacherManager Configuration.

Pydantic v2 settings loaded from environment variables (.env).
"""

from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration.
    
    Loads from environment variables and .env file.
    All values are required unless a default is provided.
    """

    # ---------- App Metadata ----------
    app_name: str = "TeacherManager"
    app_env: str = "development"  # development, staging, production
    debug: bool = True
    log_level: str = "info"

    # ---------- Server ----------
    host: str = "0.0.0.0"
    port: int = 8000
    allowed_origins: str = "http://localhost:3000,http://localhost:8000"

    # ---------- Database ----------
    database_url: str  # postgresql+asyncpg://user:pass@localhost:5432/db
    database_url_sync: str  # postgresql://user:pass@localhost:5432/db (for Alembic)

    # ---------- Redis ----------
    redis_url: str = "redis://localhost:6379/0"

    # ---------- JWT / Auth ----------
    secret_key: str  # Must be set in production
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # ---------- Sentry (APM) ----------
    sentry_dsn: Optional[str] = None
    sentry_traces_sample_rate: float = 0.2

    # ---------- Seeding ----------
    initial_admin_password: Optional[str] = None
    initial_user_password: Optional[str] = None
    force_seed_in_prod: bool = False

    # ---------- PWA / VAPID ----------
    vapid_public_key: Optional[str] = None
    vapid_private_key: Optional[str] = None

    # ---------- OAuth / SSO (optional) ----------
    oauth_client_id: Optional[str] = None
    oauth_client_secret: Optional[str] = None
    oauth_authority_url: Optional[str] = None

    # ---------- SMS (optional) ----------
    twilio_account_sid: Optional[str] = None
    twilio_auth_token: Optional[str] = None
    twilio_from_number: Optional[str] = None

    class Config:
        """Pydantic config."""

        env_file = ".env"
        case_sensitive = False

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.app_env == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.app_env == "development"

    @property
    def cors_origins(self) -> list[str]:
        """Parse ALLOWED_ORIGINS into list."""
        return [origin.strip() for origin in self.allowed_origins.split(",")]


def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# For convenience
settings = get_settings()

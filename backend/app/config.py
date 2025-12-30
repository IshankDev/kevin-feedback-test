"""Application configuration."""
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import ClassVar
from pathlib import Path
import json


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Look for .env in project root (parent of backend directory)
    env_file_path: ClassVar[Path] = Path(__file__).parent.parent.parent / ".env"
    
    model_config = SettingsConfigDict(
        env_file=str(env_file_path) if env_file_path.exists() else None,
        case_sensitive=False,
        env_file_encoding="utf-8",
        env_parse_none_str="None",
        validate_default=True
    )
    
    # Database
    database_url: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/feedback_db",
        description="PostgreSQL database connection URL"
    )
    
    # Google Gemini API
    gemini_api_key: str = Field(
        ...,
        description="Google Gemini API key",
        min_length=1
    )
    
    # CORS - can be comma-separated string or JSON array
    cors_origins: str = Field(
        default="http://localhost:5173,http://localhost:3000",
        description="Comma-separated list of allowed CORS origins"
    )
    
    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Validate database URL format."""
        if not v.startswith(("postgresql://", "postgresql+psycopg2://")):
            raise ValueError("Database URL must start with postgresql://")
        return v
    
    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins from string to list."""
        if not self.cors_origins:
            return []
        # Try JSON first, then fall back to comma-separated
        try:
            parsed = json.loads(self.cors_origins)
            return parsed if isinstance(parsed, list) else [parsed]
        except (json.JSONDecodeError, TypeError):
            return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]
    
    # App settings
    app_name: str = Field(default="Feedback Exploration API", description="Application name")
    app_version: str = Field(default="1.0.0", description="Application version")
    debug: bool = Field(default=False, description="Enable debug mode")
    api_prefix: str = Field(default="/api", description="API route prefix")
    
    # Performance settings
    database_pool_size: int = Field(default=5, ge=1, le=20, description="Database connection pool size")
    database_max_overflow: int = Field(default=10, ge=0, description="Database max overflow connections")


settings = Settings()


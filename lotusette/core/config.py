"""Configuration management for Lotusette."""

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings


# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()
DATA_DIR = PROJECT_ROOT / "lotusette" / "data"


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    app_name: str = "Lotusette"
    debug: bool = False
    log_level: str = "INFO"
    
    # LLM Configuration
    llm_provider: str = "openai"
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4-turbo-preview"
    anthropic_api_key: Optional[str] = None
    anthropic_model: str = "claude-3-opus-20240229"
    
    # Database
    database_url: str = f"sqlite:///{DATA_DIR / 'conversations' / 'lotusette.db'}"
    vector_db_type: str = "chroma"
    vector_db_url: str = "http://localhost:8000"
    
    # Redis Cache
    redis_url: str = "redis://localhost:6379"
    redis_password: Optional[str] = None
    
    # Voice Services
    stt_provider: str = "whisper"
    tts_provider: str = "coqui"
    whisper_model: str = "base"
    elevenlabs_api_key: Optional[str] = None
    
    # Web Services
    search_provider: str = "duckduckgo"
    google_search_api_key: Optional[str] = None
    google_search_engine_id: Optional[str] = None
    
    # Features
    enable_gaming: bool = False
    enable_robotics: bool = False
    
    # Security
    secret_key: str = "CHANGE-THIS-SECRET-KEY-IN-PRODUCTION-USE-ENV-FILE"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Rate Limiting
    rate_limit_per_minute: int = 60
    
    # Storage
    storage_type: str = "local"
    s3_bucket: Optional[str] = None
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    
    # Monitoring
    enable_metrics: bool = False
    prometheus_port: int = 9090
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    def validate_security(self) -> None:
        """Validate security settings."""
        if not self.debug and self.secret_key.startswith("CHANGE-THIS"):
            raise ValueError(
                "SECRET_KEY must be set to a secure random value in production. "
                "Set it in your .env file or environment variables."
            )


# Global settings instance
settings = Settings()

# Create data directories if they don't exist
os.makedirs(DATA_DIR / "conversations", exist_ok=True)
os.makedirs(DATA_DIR / "models", exist_ok=True)
os.makedirs(DATA_DIR / "embeddings", exist_ok=True)

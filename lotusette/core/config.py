"""Configuration management for Lotusette."""

import os
from pathlib import Path

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()


def _resolve_data_dir() -> Path:
    """Locate the directory holding conversations, models and embeddings.

    Les données vivent à côté du package et jamais dedans :

    1. ``LOTUSETTE_DATA_DIR`` si la variable est définie ;
    2. ``<dépôt>/data`` quand on tourne depuis une copie de travail ;
    3. sinon ``~/.local/share/lotusette``, car un paquet installé ne doit
       rien écrire dans le site-packages.
    """
    override = os.environ.get("LOTUSETTE_DATA_DIR")
    if override:
        return Path(override).expanduser().absolute()

    if (PROJECT_ROOT / "pyproject.toml").is_file():
        return PROJECT_ROOT / "data"

    xdg = os.environ.get("XDG_DATA_HOME")
    base = Path(xdg).expanduser() if xdg else Path.home() / ".local" / "share"
    return (base / "lotusette").absolute()


DATA_DIR = _resolve_data_dir()

DATA_SUBDIRS = ("conversations", "models", "embeddings")


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_name: str = "Lotusette"
    debug: bool = False
    log_level: str = "INFO"

    # LLM Configuration
    # 'local' (serveur llama.cpp / Ollama / vLLM), 'openai' ou 'claude'.
    llm_provider: str = "local"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4-turbo-preview"
    anthropic_api_key: str | None = None
    anthropic_model: str = "claude-3-opus-20240229"

    # Serveur LLM local exposant une API compatible OpenAI.
    # Les alias VLLM_* sont conservés pour ne pas casser les .env existants.
    local_llm_base_url: str = Field(
        default="http://localhost:8080/v1",
        validation_alias=AliasChoices("local_llm_base_url", "vllm_base_url"),
    )
    local_llm_model: str = Field(
        default="mistralai/Ministral-3-14B-Instruct-2512-GGUF:Q4_K_M",
        validation_alias=AliasChoices("local_llm_model", "vllm_model"),
    )
    # llama.cpp et Ollama ignorent l'en-tête d'authentification, mais l'API
    # OpenAI impose qu'il soit présent.
    local_llm_api_key: str = Field(
        default="EMPTY",
        validation_alias=AliasChoices("local_llm_api_key", "vllm_api_key"),
    )

    # Paramètres de génération.
    # Voir docs/MODELS.md : 0.6-0.8 pour la conversation libre, 0.1 pour la
    # boucle d'outils et la génération JSON.
    llm_temperature: float = 0.7
    llm_max_tokens: int = 1000
    # Nombre de messages du contexte court terme envoyés au modèle.
    # Sera remplacé par un budget en tokens à l'étape E3.
    llm_context_messages: int = 20

    # Database
    database_url: str = f"sqlite:///{DATA_DIR / 'conversations' / 'lotusette.db'}"
    vector_db_type: str = "chroma"
    vector_db_url: str = "http://localhost:8000"

    # Redis Cache
    redis_url: str = "redis://localhost:6379"
    redis_password: str | None = None

    # Voice Services
    stt_provider: str = "whisper"
    tts_provider: str = "coqui"
    whisper_model: str = "base"
    elevenlabs_api_key: str | None = None

    # Web Services
    search_provider: str = "duckduckgo"
    google_search_api_key: str | None = None
    google_search_engine_id: str | None = None

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
    s3_bucket: str | None = None
    aws_access_key_id: str | None = None
    aws_secret_access_key: str | None = None

    # Monitoring
    enable_metrics: bool = False
    prometheus_port: int = 9090

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # Ignore extra fields from .env
        populate_by_name=True,
    )

    def validate_security(self) -> None:
        """Validate security settings."""
        if not self.debug and self.secret_key.startswith("CHANGE-THIS"):
            raise ValueError(
                "SECRET_KEY must be set to a secure random value in production. "
                "Set it in your .env file or environment variables."
            )


def ensure_directories() -> None:
    """Create the data directories on disk.

    Appelée explicitement au démarrage de l'application. Importer ce module ne
    doit avoir aucun effet de bord sur le système de fichiers : les tests
    importent la configuration sans vouloir créer d'arborescence.
    """
    for subdir in DATA_SUBDIRS:
        (DATA_DIR / subdir).mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()

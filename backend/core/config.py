from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "Gerador de Relatórios"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    MAX_FILE_SIZE: int = 50 * 1024 * 1024

    ALLOWED_EXTENSIONS: list = [
        ".pdf",
        ".docx",
        ".xlsx",
        ".csv",
        ".pptx",
        ".txt",
        ".md",
    ]
    ALLOWED_MIME_TYPES: list = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "text/csv",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "text/plain",
        "text/markdown",
    ]

    LLM_PROVIDER: str = "minimax"
    LLM_MODEL: str = "minimax-m2.5"
    LLM_API_KEY: str = ""
    LLM_BASE_URL: str = "https://api.minimax.chat/v1"

    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o"

    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 8192

    SECURITY_ENABLE_GUARDRAILS: bool = True
    SECURITY_MAX_INPUT_LENGTH: int = 500000

    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:8000"]

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()

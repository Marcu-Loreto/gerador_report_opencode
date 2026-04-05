import magic
from pathlib import Path
from ..core.config import get_settings

settings = get_settings()


def validate_file(file_content: bytes, filename: str) -> None:
    if not file_content:
        raise ValueError("Arquivo vazio")

    if len(file_content) > settings.MAX_FILE_SIZE:
        raise ValueError(
            f"Arquivo excede o limite de {settings.MAX_FILE_SIZE / 1024 / 1024}MB"
        )

    ext = Path(filename).suffix.lower()
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise ValueError(
            f"Extensão {ext} não permitida. Use: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )

    mime = magic.from_buffer(file_content[:2048], mime=True)
    if mime not in settings.ALLOWED_MIME_TYPES and ext not in [".txt", ".md", ".csv"]:
        raise ValueError(f"MIME type {mime} não permitido")


def validate_extension(filename: str) -> bool:
    ext = Path(filename).suffix.lower()
    return ext in settings.ALLOWED_EXTENSIONS


def validate_size(file_content: bytes) -> bool:
    return len(file_content) <= settings.MAX_FILE_SIZE

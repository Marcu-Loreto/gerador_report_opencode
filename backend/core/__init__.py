from pathlib import Path
from typing import Optional
from .config import get_settings

settings = get_settings()


def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent


def validate_file_extension(filename: str) -> bool:
    ext = Path(filename).suffix.lower()
    return ext in settings.ALLOWED_EXTENSIONS


def validate_mime_type(mime_type: str) -> bool:
    return mime_type in settings.ALLOWED_MIME_TYPES


def get_file_type(filename: str) -> Optional[str]:
    ext = Path(filename).suffix.lower()
    mapping = {
        ".pdf": "pdf",
        ".docx": "docx",
        ".xlsx": "xlsx",
        ".csv": "csv",
        ".pptx": "pptx",
        ".txt": "txt",
        ".md": "md",
    }
    return mapping.get(ext)


def sanitize_filename(filename: str) -> str:
    import re

    filename = re.sub(r"[^\w\s.-]", "", filename)
    filename = filename.replace(" ", "_")
    return filename[:255]

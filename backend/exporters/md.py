from typing import Optional
from pathlib import Path


def export_to_markdown(content: str, filename: str = "relatorio.md") -> tuple[str, str]:
    return content, f"{Path(filename).stem}.md"


def export_to_markdown_bytes(
    content: str, filename: str = "relatorio.md"
) -> tuple[bytes, str]:
    markdown_content, fname = export_to_markdown(content, filename)
    return markdown_content.encode("utf-8"), fname

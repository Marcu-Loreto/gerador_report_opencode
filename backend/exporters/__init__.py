from .md import export_to_markdown, export_to_markdown_bytes
from .pdf import export_to_pdf, export_to_pdf_from_html
from .docx import export_to_docx, export_to_docx_with_style


def export_document(
    content: str, format: str, filename: str = "relatorio"
) -> tuple[bytes, str]:
    format = format.lower()

    if format == "md" or format == "markdown":
        content_bytes, fname = export_to_markdown(content, filename)
        return content_bytes.encode("utf-8"), fname
    elif format == "pdf":
        return export_to_pdf(content, filename)
    elif format == "docx":
        return export_to_docx(content, filename)
    else:
        raise ValueError(f"Formato não suportado: {format}")


__all__ = [
    "export_to_markdown",
    "export_to_markdown_bytes",
    "export_to_pdf",
    "export_to_pdf_from_html",
    "export_to_docx",
    "export_to_docx_with_style",
    "export_document",
]

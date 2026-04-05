from typing import Optional
from io import BytesIO
from pathlib import Path


def export_to_pdf(content: str, filename: str = "relatorio.pdf") -> tuple[bytes, str]:
    try:
        from weasyprint import HTML

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; }}
                h1 {{ color: #333; }}
                h2 {{ color: #555; }}
                pre {{ white-space: pre-wrap; word-wrap: break-word; }}
            </style>
        </head>
        <body>
            <pre>{content}</pre>
        </body>
        </html>
        """
        pdf_bytes = HTML(string=html_content).write_pdf()
        return pdf_bytes, f"{Path(filename).stem}.pdf"
    except Exception as e:
        raise RuntimeError(f"Erro ao gerar PDF: {str(e)}")


def export_to_pdf_from_html(
    html_content: str, filename: str = "relatorio.pdf"
) -> tuple[bytes, str]:
    try:
        from weasyprint import HTML

        pdf_bytes = HTML(string=html_content).write_pdf()
        return pdf_bytes, filename
    except Exception as e:
        raise RuntimeError(f"Erro ao gerar PDF: {str(e)}")

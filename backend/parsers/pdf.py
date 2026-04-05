from .base import BaseParser, ParsedDocument
import io


class PDFParser(BaseParser):
    def parse(self, content: bytes, filename: str) -> ParsedDocument:
        try:
            import PyPDF2

            reader = PyPDF2.PdfReader(io.BytesIO(content))
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"

            return ParsedDocument(
                texto=text,
                estrutura=self._detect_structure(text),
                metadados={
                    "arquivo": filename,
                    "tamanho": len(content),
                    "paginas": len(reader.pages),
                },
                alertas=[],
                limitacoes=[],
            )
        except Exception as e:
            result = self._create_empty_result(filename)
            result.alertas.append(f"Erro ao processar PDF: {str(e)}")
            result.limitacoes.append("PDF pode ter imagens ou formato não texto")
            return result

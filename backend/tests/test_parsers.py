import pytest
import io
from backend.parsers.base import BaseParser, ParsedDocument


class TestBaseParser:
    def test_detect_structure(self):
        parser = BaseParser()
        text = "# Título Principal\n\nEste é um parágrafo com muito texto.\n\n## Subtítulo\n\nMais conteúdo."
        structure = parser._detect_structure(text)
        
        assert "titulos" in structure
        assert "topicos" in structure
        assert structure["paragrafos"] > 0
    
    def test_create_empty_result(self):
        parser = BaseParser()
        result = parser._create_empty_result("test.txt")
        
        assert result.texto == ""
        assert len(result.alertas) > 0
        assert len(result.limitacoes) > 0


class TestPDFParser:
    def test_parse_invalid_pdf(self):
        from backend.parsers.pdf import PDFParser
        parser = PDFParser()
        
        content = b"Este não é um PDF válido"
        result = parser.parse(content, "test.pdf")
        
        assert result.alertas is not None
        assert result.texto is not None


class TestDOCXParser:
    def test_parse_invalid_docx(self):
        from backend.parsers.docx import DOCXParser
        parser = DOCXParser()
        
        content = b"Este não é um DOCX válido"
        result = parser.parse(content, "test.docx")
        
        assert result.alertas is not None


class TestTXTParser:
    def test_parse_text(self):
        from backend.parsers.text_parsers import TxtParser
        parser = TxtParser()
        
        content = b"Conteúdo de teste\ncom múltiplas\nlinhas"
        result = parser.parse(content, "test.txt")
        
        assert "Conteúdo de teste" in result.texto
        assert result.metadados["encoding"] in ["utf-8", "latin-1"]


class TestCSVParser:
    def test_parse_csv(self):
        from backend.parsers.xlsx import CSVParser
        parser = CSVParser()
        
        content = b"nome,idade\nJoão,30\nMaria,25"
        result = parser.parse(content, "test.csv")
        
        assert "nome" in result.texto
        assert "João" in result.texto

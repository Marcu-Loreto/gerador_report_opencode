from .base import BaseParser, ParsedDocument
from .pdf import PDFParser
from .docx import DOCXParser
from .xlsx import XLSXParser, CSVParser
from .text_parsers import PPTXParser, TxtParser, MdParser
from typing import Dict, Type


PARSERS: Dict[str, Type[BaseParser]] = {
    "pdf": PDFParser(),
    "docx": DOCXParser(),
    "xlsx": XLSXParser(),
    "csv": CSVParser(),
    "pptx": PPTXParser(),
    "txt": TxtParser(),
    "md": MdParser(),
}


def get_parser(file_type: str) -> BaseParser:
    parser = PARSERS.get(file_type.lower())
    if not parser:
        raise ValueError(f"Tipo de arquivo não suportado: {file_type}")
    return parser


def parse_document(content: bytes, file_type: str, filename: str) -> ParsedDocument:
    parser = get_parser(file_type)
    return parser.parse(content, filename)

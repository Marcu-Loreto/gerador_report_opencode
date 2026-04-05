from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Optional
import io


@dataclass
class ParsedDocument:
    texto: str
    estrutura: Dict[str, Any]
    metadados: Dict[str, Any]
    alertas: list[str]
    limitacoes: list[str]


class BaseParser(ABC):
    @abstractmethod
    def parse(self, content: bytes, filename: str) -> ParsedDocument:
        pass

    def _detect_structure(self, text: str) -> Dict[str, Any]:
        lines = text.split("\n")
        structure = {
            "titulos": [],
            "topicos": [],
            "paragrafos": len([l for l in lines if l.strip()]),
            "total_linhas": len(lines),
        }

        for i, line in enumerate(lines):
            line = line.strip()
            if line.startswith("#"):
                structure["titulos"].append(
                    {
                        "nivel": len(line) - len(line.lstrip("#")),
                        "texto": line.lstrip("#").strip(),
                    }
                )
            elif line and len(line) > 50:
                structure["topicos"].append(line[:100])

        return structure

    def _create_empty_result(self, filename: str) -> ParsedDocument:
        return ParsedDocument(
            texto="",
            estrutura={},
            metadados={"arquivo": filename, "tamanho": 0},
            alertas=["Arquivo vazio ou não foi possível extrair conteúdo"],
            limitacoes=["Extração retornou conteúdo vazio"],
        )

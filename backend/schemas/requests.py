from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum


class ReportType(str, Enum):
    RESUMO = "resumo"
    RELATORIO_TECNICO = "relatorio_tecnico"
    RELATORIO_FINEP = "relatorio_finep"
    PARECER_TECNICO = "parecer_tecnico"
    RELATO_CIENTIFICO = "relato_cientifico"
    DISSERTACAO_TESE = "dissertacao_ou_tese"


class DocumentType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    XLSX = "xlsx"
    CSV = "csv"
    PPTX = "pptx"
    TXT = "txt"
    MD = "md"


class UploadRequest(BaseModel):
    pass


class UploadResponse(BaseModel):
    request_id: str
    nome_arquivo: str
    tipo_arquivo: DocumentType
    status: str
    message: str


class AnalysisResponse(BaseModel):
    request_id: str
    nome_arquivo: str
    tipo_arquivo: DocumentType
    status_analise: str
    resumo_analitico: str
    temas_principais: List[str]
    estrutura_detectada: Dict[str, Any]
    alertas: List[str]
    limitacoes: List[str]


class GenerateReportRequest(BaseModel):
    request_id: str
    tipo_relatorio: ReportType


class GenerateReportResponse(BaseModel):
    request_id: str
    status: str
    rascunho_gerado: Optional[str] = None
    relatorio_revisado: Optional[str] = None
    message: str


class ExportRequest(BaseModel):
    request_id: str
    formato: str = Field(default="md")


class ExportResponse(BaseModel):
    request_id: str
    formato: str
    conteudo: str
    filename: str


class UpdateReportRequest(BaseModel):
    request_id: str
    conteudo: str


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    request_id: Optional[str] = None


class StepStatus(BaseModel):
    step: str
    status: str
    message: Optional[str] = None
    timestamp: Optional[str] = None

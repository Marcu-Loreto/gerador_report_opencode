from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class DocumentMetadata(BaseModel):
    tamanho: int
    formato: str
    mime_type: str
    paginas: Optional[int] = None
    linhas: Optional[int] = None
    encoding: Optional[str] = None


class ExtractionAlert(BaseModel):
    tipo: str
    mensagem: str
    severidade: str = "info"


class GraphStep(BaseModel):
    step_name: str
    status: str
    timestamp: datetime
    message: Optional[str] = None


class ReportStatusResponse(BaseModel):
    request_id: str
    status_fluxo: str
    current_step: str
    completed_steps: List[GraphStep]
    erros: List[str] = Field(default_factory=list)


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str = "1.0.0"

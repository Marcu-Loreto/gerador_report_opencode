from typing import TypedDict, Optional, List, Dict, Any
from datetime import datetime


class GraphState(TypedDict):
    request_id: str
    arquivo_original: Optional[bytes]
    nome_arquivo: str
    tipo_arquivo: str
    metadados_arquivo: Dict[str, Any]
    texto_extraido: str
    estrutura_extraida: Dict[str, Any]
    resumo_analitico: str
    alertas_extracao: List[str]
    limitacoes_extracao: List[str]
    tipo_relatorio_escolhido: str
    contexto_documental: str
    rascunho_gerado: str
    relatorio_revisado: str
    markdown_final: str
    status_fluxo: str
    logs_execucao: List[Dict[str, Any]]
    riscos_detectados: List[str]
    flags_seguranca: Dict[str, bool]
    erros: List[str]
    timestamps: Dict[str, datetime]
    edited_content: Optional[str]
    humano_interveio: bool

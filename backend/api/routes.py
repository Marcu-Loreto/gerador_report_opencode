from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import StreamingResponse
from datetime import datetime
import uuid

from ..core.config import get_settings
from ..core import get_file_type, validate_file_extension
from ..schemas.requests import (
    UploadRequest,
    UploadResponse,
    AnalysisResponse,
    GenerateReportRequest,
    GenerateReportResponse,
    ExportRequest,
    ExportResponse,
    UpdateReportRequest,
    ErrorResponse,
)
from ..schemas.responses import ReportStatusResponse, HealthResponse
from ..graph.workflow import run_workflow
from ..exporters import export_document
from ..observability.logger import get_logger
from .dependencies import session_store, SessionStore

settings = get_settings()
router = APIRouter()
logger = get_logger("api")


@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy", timestamp=datetime.now(), version=settings.APP_VERSION
    )


@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    session_store: SessionStore = Depends(lambda: session_store),
):
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="Nome de arquivo vazio")

        content = await file.read()

        validate_file_extension(file.filename)
        file_type = get_file_type(file.filename)
        if not file_type:
            raise HTTPException(status_code=400, detail="Tipo de arquivo não suportado")

        request_id = str(uuid.uuid4())

        session_store.create_session(
            request_id,
            {
                "request_id": request_id,
                "nome_arquivo": file.filename,
                "tipo_arquivo": file_type,
                "arquivo_original": content,
                "status": "uploaded",
            },
        )

        logger.info(
            f"Arquivo carregado: {file.filename}", extra={"request_id": request_id}
        )

        return UploadResponse(
            request_id=request_id,
            nome_arquivo=file.filename,
            tipo_arquivo=file_type,
            status="uploaded",
            message="Arquivo carregado com sucesso",
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Erro no upload: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao processar upload")


@router.post("/analyze/{request_id}", response_model=AnalysisResponse)
async def analyze_document(
    request_id: str, session_store: SessionStore = Depends(lambda: session_store)
):
    session = session_store.get_session(request_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    try:
        from ..parsers import parse_document
        from ..agents import INGESTION_AGENT

        content = session["arquivo_original"]
        nome_arquivo = session["nome_arquivo"]
        tipo_arquivo = session["tipo_arquivo"]

        parsed = parse_document(content, tipo_arquivo, nome_arquivo)

        task = f"""Analise o documento e forneça:
1. Resumo analítico
2. Principais temas
3. Estrutura detectada

Documento:
{parsed.texto[:5000]}"""

        analise = INGESTION_AGENT.execute(parsed.texto, task)

        session_store.update_session(
            request_id,
            {
                "texto_extraido": parsed.texto,
                "estrutura_extraida": parsed.estrutura,
                "metadados_arquivo": parsed.metadados,
                "alertas_extracao": parsed.alertas,
                "limitacoes_extracao": parsed.limitacoes,
                "resumo_analitico": analise,
                "status": "analyzed",
            },
        )

        return AnalysisResponse(
            request_id=request_id,
            nome_arquivo=nome_arquivo,
            tipo_arquivo=tipo_arquivo,
            status_analise="completed",
            resumo_analitico=analise,
            temas_principais=parsed.estrutura.get("topicos", [])[:5],
            estrutura_detectada=parsed.estrutura,
            alertas=parsed.alertas,
            limitacoes=parsed.limitacoes,
        )

    except Exception as e:
        logger.error(f"Erro na análise: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate", response_model=GenerateReportResponse)
async def generate_report(
    request: GenerateReportRequest,
    session_store: SessionStore = Depends(lambda: session_store),
):
    session = session_store.get_session(request.request_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    try:
        session_store.update_session(
            request.request_id,
            {
                "tipo_relatorio_escolhido": request.tipo_relatorio,
                "status": "generating",
            },
        )

        final_state = run_workflow(
            request_id=request.request_id,
            arquivo_original=session["arquivo_original"],
            nome_arquivo=session["nome_arquivo"],
            tipo_arquivo=session["tipo_arquivo"],
            tipo_relatorio=request.tipo_relatorio,
        )

        session_store.update_session(
            request.request_id,
            {
                "rascunho_gerado": final_state.get("rascunho_gerado", ""),
                "relatorio_revisado": final_state.get("relatorio_revisado", ""),
                "markdown_final": final_state.get("markdown_final", ""),
                "logs_execucao": final_state.get("logs_execucao", []),
                "status": final_state.get("status_fluxo", "completed"),
            },
        )

        return GenerateReportResponse(
            request_id=request.request_id,
            status="completed",
            rascunho_gerado=final_state.get("rascunho_gerado"),
            relatorio_revisado=final_state.get("relatorio_revisado"),
            message="Relatório gerado com sucesso",
        )

    except Exception as e:
        logger.error(f"Erro na geração: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{request_id}", response_model=ReportStatusResponse)
async def get_status(
    request_id: str, session_store: SessionStore = Depends(lambda: session_store)
):
    session = session_store.get_session(request_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return ReportStatusResponse(
        request_id=request_id,
        status_fluxo=session.get("status", "unknown"),
        current_step=session.get("current_step", ""),
        completed_steps=session.get("logs_execucao", []),
        erros=session.get("erros", []),
    )


@router.get("/result/{request_id}")
async def get_result(
    request_id: str, session_store: SessionStore = Depends(lambda: session_store)
):
    session = session_store.get_session(request_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    content = session.get("relatorio_revisado") or session.get("markdown_final") or ""
    return {"request_id": request_id, "content": content}


@router.post("/export")
async def export_report(
    request: ExportRequest, session_store: SessionStore = Depends(lambda: session_store)
):
    session = session_store.get_session(request.request_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    content = session.get("relatorio_revisado") or session.get("markdown_final") or ""

    try:
        content_bytes, filename = export_document(
            content, request.formato, session.get("nome_arquivo", "relatorio")
        )

        media_type = {
            "md": "text/markdown",
            "pdf": "application/pdf",
            "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        }.get(request.formato, "application/octet-stream")

        return StreamingResponse(
            iter([content_bytes]),
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )

    except Exception as e:
        logger.error(f"Erro na exportação: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/update")
async def update_report(
    request: UpdateReportRequest,
    session_store: SessionStore = Depends(lambda: session_store),
):
    session = session_store.get_session(request.request_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    session_store.update_session(
        request.request_id,
        {
            "edited_content": request.conteudo,
            "humano_interveio": True,
            "status": "edited",
        },
    )

    return {"request_id": request.request_id, "status": "updated"}


@router.delete("/session/{request_id}")
async def delete_session(
    request_id: str, session_store: SessionStore = Depends(lambda: session_store)
):
    session_store.delete_session(request_id)
    return {"status": "deleted", "request_id": request_id}

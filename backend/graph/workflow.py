from typing import Literal
from langgraph.graph import StateGraph, END
from datetime import datetime
import uuid

from .state import GraphState
from ..parsers import parse_document
from ..agents import (
    get_agent,
    INGESTION_AGENT,
    TECHNICAL_REPORT_AGENT,
    FINEP_REPORT_AGENT,
    TECHNICAL_OPINION_AGENT,
    SCIENTIFIC_REPORT_AGENT,
    FINAL_REVIEWER_AGENT,
)
from ..security.guardrails import check_security_risks
from ..security.sanitizer import sanitize_input
from ..validators.input_validator import validate_file


def create_initial_state(
    request_id: str, arquivo_original: bytes, nome_arquivo: str, tipo_arquivo: str
) -> GraphState:
    return GraphState(
        request_id=request_id,
        arquivo_original=arquivo_original,
        nome_arquivo=nome_arquivo,
        tipo_arquivo=tipo_arquivo,
        metadados_arquivo={},
        texto_extraido="",
        estrutura_extraida={},
        resumo_analitico="",
        alertas_extracao=[],
        limitacoes_extracao=[],
        tipo_relatorio_escolhido="",
        contexto_documental="",
        rascunho_gerado="",
        relatorio_revisado="",
        markdown_final="",
        status_fluxo="iniciado",
        logs_execucao=[],
        riscos_detectados=[],
        flags_seguranca={},
        erros=[],
        timestamps={"inicio": datetime.now()},
        edited_content=None,
        humano_interveio=False,
    )


def add_log(
    state: GraphState, step: str, message: str, status: str = "success"
) -> GraphState:
    state["logs_execucao"].append(
        {
            "step": step,
            "message": message,
            "status": status,
            "timestamp": datetime.now().isoformat(),
        }
    )
    return state


def validate_upload_node(state: GraphState) -> GraphState:
    try:
        validate_file(state["arquivo_original"], state["nome_arquivo"])
        state = add_log(state, "validate_upload", "Upload validado com sucesso")
        state["status_fluxo"] = "validado"
    except Exception as e:
        state = add_log(state, "validate_upload", str(e), "error")
        state["erros"].append(str(e))
        state["status_fluxo"] = "erro_validacao"
    return state


def parse_document_node(state: GraphState) -> GraphState:
    try:
        parsed = parse_document(
            state["arquivo_original"], state["tipo_arquivo"], state["nome_arquivo"]
        )
        state["texto_extraido"] = parsed.texto
        state["estrutura_extraida"] = parsed.estrutura
        state["metadados_arquivo"] = parsed.metadados
        state["alertas_extracao"] = parsed.alertas
        state["limitacoes_extracao"] = parsed.limitacoes

        state = add_log(
            state,
            "parse_document",
            f"Documento parseado: {len(parsed.texto)} caracteres",
        )
        state["status_fluxo"] = "parseado"
    except Exception as e:
        state = add_log(state, "parse_document", str(e), "error")
        state["erros"].append(str(e))
        state["status_fluxo"] = "erro_parsing"
    return state


def security_precheck_node(state: GraphState) -> GraphState:
    try:
        sanitized_text = sanitize_input(state["texto_extraido"])
        state["texto_extraido"] = sanitized_text

        risks = check_security_risks(state["texto_extraido"])
        state["riscos_detectados"] = risks
        state["flags_seguranca"] = {
            "injection_detected": len(risks) > 0,
            "content_sanitized": True,
        }

        if risks:
            state = add_log(
                state, "security_precheck", f"Riscos detectados: {risks}", "warning"
            )
        else:
            state = add_log(
                state, "security_precheck", "Conteúdo validado com segurança"
            )

        state["status_fluxo"] = "seguranca_verificada"
    except Exception as e:
        state = add_log(state, "security_precheck", str(e), "error")
        state["erros"].append(str(e))
        state["status_fluxo"] = "erro_seguranca"
    return state


def document_analysis_node(state: GraphState) -> GraphState:
    try:
        task = f"""Analise o seguinte documento ({state["nome_arquivo"]}) e forneça:
1. Um resumo analítico do conteúdo
2. Os principais temas abordados
3. A estrutura detectada (títulos, seções, tópicos)
4. Alertas sobre qualidade ou possíveis problemas
5. Limitações na extração

Documento:
{state["texto_extraido"][:10000]}"""

        result = INGESTION_AGENT.execute(context=state["texto_extraido"], task=task)

        state["resumo_analitico"] = result
        state["contexto_documental"] = state["texto_extraido"]

        state = add_log(state, "document_analysis", "Análise documental concluída")
        state["status_fluxo"] = "analisado"
    except Exception as e:
        state = add_log(state, "document_analysis", str(e), "error")
        state["erros"].append(str(e))
        state["status_fluxo"] = "erro_analise"
    return state


def route_report_type_node(state: GraphState) -> GraphState:
    report_type = state["tipo_relatorio_escolhido"]
    state = add_log(state, "route_report_type", f"Roteando para: {report_type}")
    return state


def technical_report_node(state: GraphState) -> GraphState:
    try:
        task = f"""Gere um RELATÓRIO TÉCNICO completo e profissional baseado no documento analisado.

O relatório deve conter:
- Objetivo
- Contexto
- Escopo
- Metodologia
- Análise dos Achados
- Riscos Identificados
- Conclusões
- Recomendações

Use linguagem técnica, clara e orientada a decisão.

Documento base:
{state["contexto_documental"][:15000]}"""

        result = TECHNICAL_REPORT_AGENT.execute(
            context=state["resumo_analitico"], task=task
        )

        state["rascunho_gerado"] = result
        state = add_log(state, "technical_report", "Relatório técnico gerado")
        state["status_fluxo"] = "relatorio_gerado"
    except Exception as e:
        state = add_log(state, "technical_report", str(e), "error")
        state["erros"].append(str(e))
        state["status_fluxo"] = "erro_relatorio"
    return state


def finep_report_node(state: GraphState) -> GraphState:
    try:
        task = f"""Gere um RELATÓRIO NO ESTILO FINEP para submeter a organisme de fomento.

O relatório deve conter:
- Justificativa e Contextualização
- Problema e Oportunidade
- Inovação e Diferencial
- Relevância e Impacto
- Metodologia Proposta
- Riscos e Mitigações
- Resultados Esperados
- Indicadores de Sucesso
- Impacto e Sustentabilidade
- Conclusões

Use linguagem técnico-institucional formal.

Documento base:
{state["contexto_documental"][:15000]}"""

        result = FINEP_REPORT_AGENT.execute(
            context=state["resumo_analitico"], task=task
        )

        state["rascunho_gerado"] = result
        state = add_log(state, "finep_report", "Relatório FINEP gerado")
        state["status_fluxo"] = "relatorio_gerado"
    except Exception as e:
        state = add_log(state, "finep_report", str(e), "error")
        state["erros"].append(str(e))
        state["status_fluxo"] = "erro_relatorio"
    return state


def technical_opinion_node(state: GraphState) -> GraphState:
    try:
        task = f"""Gere um PARECER TÉCNICO formal e fundamentado.

O parecer deve conter:
- Identificação do Objeto Analisado
- Fundamentos e Metodologia
- Análise de Conformidades
- Análise de Não Conformidades
- Riscos e Impactos
- Recomendação Final

Use linguagem assertiva e tecnicamente justificável.

Documento base:
{state["contexto_documental"][:15000]}"""

        result = TECHNICAL_OPINION_AGENT.execute(
            context=state["resumo_analitico"], task=task
        )

        state["rascunho_gerado"] = result
        state = add_log(state, "technical_opinion", "Parecer técnico gerado")
        state["status_fluxo"] = "relatorio_gerado"
    except Exception as e:
        state = add_log(state, "technical_opinion", str(e), "error")
        state["erros"].append(str(e))
        state["status_fluxo"] = "erro_relatorio"
    return state


def scientific_report_node(state: GraphState) -> GraphState:
    try:
        is_long = state["tipo_relatorio_escolhido"] == "dissertacao_ou_tese"
        task_suffix = ""

        if is_long:
            task_suffix = """
Este documento deve ser estruturado como uma DISSERTAÇÃO ou TESE de doutorado, com:
- Introdução elaborada
- Revisão de Literatura
- Problema e Objetivos
- Fundamentação Teórica
- Metodologia
- Análise e Discussão
- Conclusões
- Trabalhos Futuros
- Referências (sugeridas)
"""
        else:
            task_suffix = """
Este documento deve ser estruturado como RELATÓRIO CIENTÍFICO/ACADÊMICO, com:
- Resumo
- Introdução
- Problema e Objetivos
- Fundamentação Teórica
- Metodologia
- Resultados e Discussão
- Conclusões
- Referências (sugeridas)
"""

        task = f"""Gere um RELATO CIENTÍFICO/ACADÊMICO.{task_suffix}

Use linguagem formal acadêmica, rigor metodológico e coherência argumentativa.

Documento base:
{state["contexto_documental"][:20000]}"""

        result = SCIENTIFIC_REPORT_AGENT.execute(
            context=state["resumo_analitico"], task=task
        )

        state["rascunho_gerado"] = result
        state = add_log(state, "scientific_report", "Relato científico gerado")
        state["status_fluxo"] = "relatorio_gerado"
    except Exception as e:
        state = add_log(state, "scientific_report", str(e), "error")
        state["erros"].append(str(e))
        state["status_fluxo"] = "erro_relatorio"
    return state


def quality_validation_node(state: GraphState) -> GraphState:
    content = state.get("edited_content") or state.get("rascunho_gerado", "")

    if len(content) < 100:
        state["erros"].append("Conteúdo gerado muito curto ou vazio")
        state = add_log(state, "quality_validation", "Conteúdo insuficiente", "error")
        state["status_fluxo"] = "erro_qualidade"
        return state

    if not content.strip():
        state["erros"].append("Conteúdo vazio após processamento")
        state = add_log(state, "quality_validation", "Conteúdo vazio", "error")
        state["status_fluxo"] = "erro_qualidade"
        return state

    state = add_log(state, "quality_validation", "Validação de qualidade aprovada")
    state["status_fluxo"] = "qualidade_validada"
    return state


def final_reviewer_node(state: GraphState) -> GraphState:
    try:
        content = state.get("edited_content") or state.get("rascunho_gerado", "")

        task = f"""Revise o seguinte documento, corrigindo:
- Incoerências e contradições
- Redundâncias
- Falhas de estrutura
- Erros gramaticais e de pontuação
- Inadequações de tom
- Problemas de formatação

O documento revisado deve manter o significado original, mas com melhor legibilidade e qualidade textual.

Documento original:
{content}"""

        result = FINAL_REVIEWER_AGENT.execute(context=content, task=task)

        state["relatorio_revisado"] = result
        state = add_log(state, "final_reviewer", "Revisão final concluída")
        state["status_fluxo"] = "revisado"
    except Exception as e:
        state = add_log(state, "final_reviewer", str(e), "error")
        state["erros"].append(str(e))
        state["relatorio_revisado"] = state.get("rascunho_gerado", "")
        state["status_fluxo"] = "revisado_com_erro"
    return state


def human_edit_checkpoint_node(state: GraphState) -> GraphState:
    if state.get("edited_content"):
        state["humano_interveio"] = True
        state = add_log(state, "human_edit", "Edição humana aplicada")
    else:
        state = add_log(
            state, "human_edit", "Sem edição humana, usando revisão automática"
        )
    state["status_fluxo"] = "pronto_para_exportar"
    return state


def markdown_render_node(state: GraphState) -> GraphState:
    content = state.get("relatorio_revisado") or state.get("rascunho_gerado", "")
    state["markdown_final"] = content
    state = add_log(state, "markdown_render", "Markdown preparado para exportação")
    state["status_fluxo"] = "formatado"
    return state


def finalize_response_node(state: GraphState) -> GraphState:
    state["timestamps"]["finalizacao"] = datetime.now()
    state["status_fluxo"] = "finalizado"
    state = add_log(state, "finalize", "Fluxo concluído com sucesso")
    return state


def should_route_to_report(state: GraphState) -> Literal["generate_report", "error"]:
    if state["status_fluxo"] in [
        "erro_validacao",
        "erro_parsing",
        "erro_seguranca",
        "erro_analise",
    ]:
        return "error"
    return "generate_report"


def route_by_report_type(state: GraphState) -> str:
    report_type = state["tipo_relatorio_escolhido"]
    routes = {
        "relatorio_tecnico": "technical_report",
        "relatorio_finep": "finep_report",
        "parecer_tecnico": "technical_opinion",
        "relato_cientifico": "scientific_report",
        "dissertacao_ou_tese": "scientific_report",
    }
    return routes.get(report_type, "technical_report")


def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("validate_upload", validate_upload_node)
    graph.add_node("parse_document", parse_document_node)
    graph.add_node("security_precheck", security_precheck_node)
    graph.add_node("document_analysis", document_analysis_node)
    graph.add_node("route_report_type", route_report_type_node)
    graph.add_node("technical_report", technical_report_node)
    graph.add_node("finep_report", finep_report_node)
    graph.add_node("technical_opinion", technical_opinion_node)
    graph.add_node("scientific_report", scientific_report_node)
    graph.add_node("quality_validation", quality_validation_node)
    graph.add_node("final_reviewer", final_reviewer_node)
    graph.add_node("human_edit_checkpoint", human_edit_checkpoint_node)
    graph.add_node("markdown_render", markdown_render_node)
    graph.add_node("finalize_response", finalize_response_node)

    graph.set_entry_point("validate_upload")

    graph.add_edge("validate_upload", "parse_document")
    graph.add_edge("parse_document", "security_precheck")
    graph.add_edge("security_precheck", "document_analysis")
    graph.add_edge("document_analysis", "route_report_type")

    graph.add_conditional_edges(
        "route_report_type",
        route_by_report_type,
        {
            "technical_report": "technical_report",
            "finep_report": "finep_report",
            "technical_opinion": "technical_opinion",
            "scientific_report": "scientific_report",
        },
    )

    graph.add_edge("technical_report", "quality_validation")
    graph.add_edge("finep_report", "quality_validation")
    graph.add_edge("technical_opinion", "quality_validation")
    graph.add_edge("scientific_report", "quality_validation")

    graph.add_conditional_edges(
        "quality_validation",
        should_route_to_report,
        {"generate_report": "final_reviewer", "error": END},
    )

    graph.add_edge("final_reviewer", "human_edit_checkpoint")
    graph.add_edge("human_edit_checkpoint", "markdown_render")
    graph.add_edge("markdown_render", "finalize_response")
    graph.add_edge("finalize_response", END)

    return graph.compile()


def run_workflow(
    request_id: str,
    arquivo_original: bytes,
    nome_arquivo: str,
    tipo_arquivo: str,
    tipo_relatorio: str,
) -> GraphState:
    initial_state = create_initial_state(
        request_id=request_id,
        arquivo_original=arquivo_original,
        nome_arquivo=nome_arquivo,
        tipo_arquivo=tipo_arquivo,
    )
    initial_state["tipo_relatorio_escolhido"] = tipo_relatorio

    graph = build_graph()
    final_state = graph.invoke(initial_state)
    return final_state

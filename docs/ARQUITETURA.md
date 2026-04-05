# Gerador de Relatórios Especializados - Arquitetura Multiagente

## 1. Visão Geral da Solução

Sistema web para geração de relatórios especializados a partir de documentos uploadedos, utilizando arquitetura multiagente baseada em LangGraph com revisão obrigatória.

### Fluxo Principal
1. Upload de documento (.docx, .csv, .xlsx, .pdf, .txt, .pptx, .md)
2. Análise e extração de conteúdo
3. Seleção do tipo de relatório
4. Geração por agente especializado
5. Revisão final obrigatória
6. Edição humana
7. Exportação (.md, .pdf, .docx)

---

## 2. Requisitos Funcionais

| ID | Requisito | Descrição |
|----|-----------|-----------|
| RF-01 | Upload de documentos | Aceitar arquivos .docx, .csv, .xlsx, .pdf, .txt, .pptx, .md |
| RF-02 | Análise documental | Extrair texto, estrutura, metadados e gerar resumo analítico |
| RF-03 | Tipos de relatório | Gerar: resumo, relatório técnico, FINEP, parecer técnico, relato científico, dissertação/tese |
| RF-04 | Revisão obrigatória | Todo conteúdo passa por agente revisor antes da entrega |
| RF-05 | Edição humana | Usuário pode editar antes da exportação final |
| RF-06 | Exportação | Exportar em .md, .pdf, .docx |
| RF-07 | Feedback visual | Exibir progresso por etapa do LangGraph |

---

## 3. Requisitos Não Funcionais

| ID | Requisito | Critério |
|----|-----------|----------|
| RNF-01 | Segurança | Guardrails contra prompt injection, conteúdo malicioso |
| RNF-02 | Rastreabilidade | Logs por request_id e etapa do grafo |
| RNF-03 | Responsividade | Interface usável em desktop e mobile |
| RNF-04 | Dark/Light Mode | Suporte a ambos os temas |
| RNF-05 | Testabilidade | Cobertura de testes unitários, funcionais e de segurança |

---

## 4. Arquitetura da Aplicação

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React + TS)                   │
│  ┌──────────┐  ┌────────────────┐  ┌────────────────────────┐  │
│  │  Upload  │  │   Editor/       │  │  Export & Preview      │  │
│  │  Panel   │  │   Preview       │  │  Panel                 │  │
│  └──────────┘  └────────────────┘  └────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │ HTTP/WebSocket
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                     BACKEND (FastAPI + LangGraph)              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │
│  │   API    │  │  Agents  │  │  Graph   │  │  Exporters   │   │
│  │  Layer   │  │  Layer   │  │  Orch.   │  │  Layer       │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Security & Guardrails Layer                 │   │
│  └─────────────────────────────────────────────────────────┘   │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    LLM Provider (MiniMax/OpenAI)                │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. Arquitetura LangGraph

### Estado do Grafo
```python
GraphState = {
    "request_id": str,
    "arquivo_original": bytes,
    "nome_arquivo": str,
    "tipo_arquivo": str,
    "metadados_arquivo": dict,
    "texto_extraido": str,
    "estrutura_extraida": dict,
    "resumo_analitico": str,
    "alertas_extracao": list[str],
    "limitacoes_extracao": list[str],
    "tipo_relatorio_escolhido": str,
    "contexto_documental": str,
    "rascunho_gerado": str,
    "relatorio_revisado": str,
    "markdown_final": str,
    "status_fluxo": str,
    "logs_execucao": list[dict],
    "riscos_detectados": list[str],
    "flags_seguranca": dict,
    "erros": list[str],
    "timestamps": dict
}
```

### Nós do Grafo
1. `validate_upload_node` - Valida formato, tamanho, MIME
2. `parse_document_node` - Executa parsing conforme tipo
3. `security_precheck_node` - Analisa riscos de injeção
4. `document_analysis_node` - Análise e resumo inicial
5. `route_report_type_node` - Roteia para agente apropriado
6. `technical_report_node` - Gera relatório técnico
7. `finep_report_node` - Gera relatório FINEP
8. `technical_opinion_node` - Gera parecer técnico
9. `scientific_report_node` - Gera relato científico
10. `quality_validation_node` - Valida estrutura antes da revisão
11. `final_reviewer_node` - Revisa e corrige documento
12. `markdown_render_node` - Prepara saída final
13. `human_edit_checkpoint_node` - Permite intervenção humana
14. `finalize_response_node` - Retorna payload final

---

## 6. Estrutura de Diretórios

```
gerador_report_opencode/
├── backend/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py          # Endpoints FastAPI
│   │   └── dependencies.py    # Dependências injetadas
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py          # Configurações .env
│   ├── graph/
│   │   ├── __init__.py
│   │   ├── state.py           # TypedDict do estado
│   │   └── workflow.py        # Compilação do grafo
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base.py            # Agente base
│   │   ├── ingestion.py       # Agente de análise
│   │   ├── technical.py       # Relatório técnico
│   │   ├── finep.py          # Relatório FINEP
│   │   ├── opinion.py        # Parecer técnico
│   │   ├── scientific.py      # Relato científico
│   │   └── reviewer.py        # Revisor final
│   ├── parsers/
│   │   ├── __init__.py
│   │   ├── base.py           # Parser base
│   │   ├── pdf.py
│   │   ├── docx.py
│   │   ├── xlsx.py
│   │   ├── csv.py
│   │   ├── pptx.py
│   │   ├── txt.py
│   │   └── md.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── requests.py        # Modelos de request
│   │   └── responses.py      # Modelos de response
│   ├── services/
│   │   ├── __init__.py
│   │   └── llm_service.py    # Serviço LLM
│   ├── exporters/
│   │   ├── __init__.py
│   │   ├── md.py
│   │   ├── pdf.py
│   │   └── docx.py
│   ├── security/
│   │   ├── __init__.py
│   │   ├── guardrails.py     # Guardrails de segurança
│   │   └── sanitizer.py      # Sanitização de texto
│   ├── validators/
│   │   ├── __init__.py
│   │   └── input_validator.py
│   ├── observability/
│   │   ├── __init__.py
│   │   └── logger.py         # Logs estruturados
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_parsers.py
│   │   ├── test_security.py
│   │   └── test_graph.py
│   ├── main.py               # Entry point FastAPI
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileUploadPanel.tsx
│   │   │   ├── DocumentStatusCard.tsx
│   │   │   ├── ReportTypeSelector.tsx
│   │   │   ├── ProcessingStepper.tsx
│   │   │   ├── SecurityAlertsBanner.tsx
│   │   │   ├── AnalysisSummaryCard.tsx
│   │   │   ├── ReportEditor.tsx
│   │   │   ├── MarkdownPreview.tsx
│   │   │   ├── ExportActions.tsx
│   │   │   ├── ThemeToggle.tsx
│   │   │   └── index.ts
│   │   ├── hooks/
│   │   │   ├── useUpload.ts
│   │   │   ├── useReportGeneration.ts
│   │   │   └── useTheme.ts
│   │   ├── services/
│   │   │   └── api.ts
│   │   ├── types/
│   │   │   └── index.ts
│   │   ├── utils/
│   │   │   └── helpers.ts
│   │   ├── styles/
│   │   │   └── globals.css
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── README.md
├── .gitignore
└── docker-compose.yml
```

---

## 7-15. Implementação

A implementação detalhada será criada nos próximos passos.

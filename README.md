# Gerador de Relatórios Especializados

Aplicação web completa para geração de relatórios especializados a partir de documentos, utilizando arquitetura multiagente baseada em LangGraph com revisão obrigatória.

## 🚀 Funcionalidades

- **Upload de Documentos**: Suporte a PDF, DOCX, XLSX, CSV, PPTX, TXT, MD
- **Análise Documental**: Extração de texto, estrutura e geração de resumo analítico
- **Geração de Relatórios**:
  - Relatório Técnico
  - Relatório FINEP (padrão de organismos de fomento)
  - Parecer Técnico
  - Relato Científico/Acadêmico
  - Dissertação/Tese
- **Revisão Obrigatória**: Todo conteúdo passa por agente revisor final
- **Edição Humana**: Permite edição antes da exportação
- **Exportação**: Markdown, PDF, DOCX
- **Segurança**: Guardrails contra prompt injection e conteúdo malicioso
- **Dark Mode**: Suporte a tema claro e escuro

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│ Frontend (React + TypeScript + TailwindCSS)                 │
│ - Componentes React                                         │
│ - Hooks para gerenciamento de estado                       │
│ - Integração com API via Axios                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ Backend (Python + FastAPI + LangGraph)                     │
│ - API RESTful                                               │
│ - Orquestrador LangGraph                                    │
│ - Agentes especializados                                   │
│ - Parsers documentais                                      │
│ - Guardrails de segurança                                  │
│ - Sistema de exportação                                    │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Estrutura do Projeto

```
gerador_report_opencode/
├── backend/
│   ├── api/           # Rotas FastAPI
│   ├── core/          # Configurações
│   ├── graph/         # Estado e workflow LangGraph
│   ├── agents/        # Agentes especializados
│   ├── parsers/       # Parsers por tipo de arquivo
│   ├── schemas/       # Modelos Pydantic
│   ├── services/      # Serviço LLM
│   ├── exporters/     # Exportação MD/PDF/DOCX
│   ├── security/      # Guardrails e sanitização
│   ├── validators/    # Validação de entrada
│   ├── observability/ # Logs estruturados
│   ├── tests/         # Testes automatizados
│   └── main.py        # Entry point
├── frontend/
│   ├── src/
│   │   ├── components/  # Componentes React
│   │   ├── hooks/       # Hooks personalizados
│   │   ├── services/    # API client
│   │   ├── types/       # Tipos TypeScript
│   │   └── styles/      # Estilos CSS
│   └── package.json
├── docs/
│   └── ARQUITETURA.md  # Documentação arquitetural
└── README.md
```

## 🛠️ Instalação

### Pré-requisitos

- Python 3.10+
- Node.js 18+
- npm ou yarn

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

### Configuração

Crie um arquivo `.env` no diretório `backend/`:

```env
# Configurações do App
APP_NAME=Gerador de Relatórios
APP_VERSION=1.0.0
DEBUG=false

# Limites
MAX_FILE_SIZE=52428800

# LLM (MiniMax)
LLM_PROVIDER=minimax
LLM_API_KEY=your_minimax_api_key
LLM_BASE_URL=https://api.minimax.chat/v1

# ou OpenAI
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# CORS
CORS_ORIGINS=["http://localhost:5173","http://localhost:8000"]
```

## ▶️ Execução

### Backend

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm run dev
```

Acesse: http://localhost:5173

## 🔧 Desenvolvimento

### Executar Testes

```bash
# Backend
cd backend
pytest tests/ -v

# Com cobertura
pytest tests/ --cov=. --cov-report=html
```

### Build para Produção

```bash
# Frontend
cd frontend
npm run build
```

## 📡 API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/v1/upload` | Upload de arquivo |
| POST | `/api/v1/analyze/{request_id}` | Analisar documento |
| POST | `/api/v1/generate` | Gerar relatório |
| GET | `/api/v1/status/{request_id}` | Verificar status |
| GET | `/api/v1/result/{request_id}` | Obter resultado |
| POST | `/api/v1/export` | Exportar relatório |
| POST | `/api/v1/update` | Atualizar conteúdo |

## 🛡️ Segurança

- Validação de MIME type e extensão
- Limite de tamanho de arquivo
- Sanitização de entrada
- Detecção de prompt injection
- Separação entre instruções do sistema e conteúdo do usuário

## 📝 Licença

MIT

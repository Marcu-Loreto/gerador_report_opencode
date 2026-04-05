#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
export PYTHONPATH=/l/disk0/marcub/Documentos/apps/Gerador_relatorio_opencode/backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

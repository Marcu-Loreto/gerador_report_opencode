#!/bin/bash

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"

echo "=== Criando ambiente virtual ==="
cd "$PROJECT_ROOT"

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "Ambiente virtual criado em: $PROJECT_ROOT/.venv"
fi

echo "=== Ativando ambiente virtual ==="
source .venv/bin/activate

echo "=== Instalando dependências ==="
pip install --upgrade pip
pip install -r backend/requirements.txt

echo "=== Configurando variáveis de ambiente ==="
if [ ! -f .env ]; then
    cp .env_example .env
    echo "Arquivo .env criado. Configure suas API keys!"
fi

echo "=== Iniciando servidor ==="
cd "$PROJECT_ROOT"
PYTHONPATH="$PROJECT_ROOT/backend" uvicorn backend.main:app --host 0.0.0.0 --port 8000

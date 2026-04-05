FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libmagic1 \
    libpoppler-cpp-dev \
    libpoppler-utils \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN python3 -m venv /app/.venv && \
    /app/.venv/bin/pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app/backend
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["/app/.venv/bin/python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]

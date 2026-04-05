from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .core.config import get_settings
from .api.routes import router
from .observability.logger import get_logger

settings = get_settings()
logger = get_logger("main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Iniciando {settings.APP_NAME} v{settings.APP_VERSION}")
    yield
    logger.info("Encerrando aplicação")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Gerador de relatórios especializados com arquitetura multiagente",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1", tags=["gerador-relatorios"])


@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }

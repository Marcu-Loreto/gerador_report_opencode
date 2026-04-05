from typing import Optional


def get_llm_service():
    pass


def get_llm_service():
    from ..services.llm_service import get_llm_service as _get_llm_service

    return _get_llm_service()


__all__ = ["get_llm_service"]

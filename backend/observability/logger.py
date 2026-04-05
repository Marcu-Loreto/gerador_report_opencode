import logging
import json
from datetime import datetime
from typing import Any, Dict
from functools import lru_cache

from ..core.config import get_settings

settings = get_settings()


class StructuredLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, settings.LOG_LEVEL))

        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )
            )
            self.logger.addHandler(handler)

    def log(self, level: str, message: str, extra: Dict[str, Any] = None):
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "message": message,
            **extra,
        }
        getattr(self.logger, level)(json.dumps(log_data))

    def info(self, message: str, **extra):
        self.log("info", message, extra)

    def warning(self, message: str, **extra):
        self.log("warning", message, extra)

    def error(self, message: str, **extra):
        self.log("error", message, extra)


@lru_cache()
def get_logger(name: str = "app") -> StructuredLogger:
    return StructuredLogger(name)


def log_request(request_id: str, step: str, status: str, message: str = ""):
    logger = get_logger()
    logger.info(
        f"[{request_id}] {step}",
        extra={
            "request_id": request_id,
            "step": step,
            "status": status,
            "message": message,
        },
    )

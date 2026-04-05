from typing import Optional, Dict, Any, Literal
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from ..core.config import get_settings

settings = get_settings()

TaskComplexity = Literal["simple", "medium", "complex"]

TASK_COMPLEXITY_MAP: Dict[str, TaskComplexity] = {
    "technical_report": "medium",
    "finep_report": "complex",
    "technical_opinion": "medium",
    "scientific_report": "complex",
    "dissertacao_ou_tese": "complex",
    "ingestion": "simple",
    "final_reviewer": "medium",
    "quality_validation": "simple",
}


def _get_client_for_task(task_type: str = "default"):
    complexity = TASK_COMPLEXITY_MAP.get(task_type, "medium")

    if complexity == "simple":
        if settings.LLM_API_KEY and settings.LLM_BASE_URL:
            return ChatOpenAI(
                model="MiniMax-M2.5",
                api_key=settings.LLM_API_KEY,
                base_url=settings.LLM_BASE_URL,
                temperature=settings.TEMPERATURE,
                max_tokens=settings.MAX_TOKENS,
            )
        else:
            return ChatOpenAI(
                model=settings.OPENAI_MODEL,
                api_key=settings.OPENAI_API_KEY,
                temperature=settings.TEMPERATURE,
                max_tokens=settings.MAX_TOKENS,
            )
    elif complexity == "complex":
        return ChatOpenAI(
            model=settings.OPENAI_MODEL_COMPLEX,
            api_key=settings.OPENAI_API_KEY,
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_TOKENS,
        )
    else:
        return ChatOpenAI(
            model=settings.OPENAI_MODEL,
            api_key=settings.OPENAI_API_KEY,
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_TOKENS,
        )


class LLMService:
    def __init__(
        self,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        complexity: Optional[TaskComplexity] = None,
    ):
        self.provider = provider or settings.LLM_PROVIDER
        self.complexity = complexity or "medium"
        self._model = model
        self._client = None

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        task_type: str = "default",
    ) -> str:
        client = _get_client_for_task(task_type)

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]

        params = {}
        if temperature is not None:
            params["temperature"] = temperature
        if max_tokens is not None:
            params["max_tokens"] = max_tokens

        response = client.invoke(messages, **params)
        return response.content

    def generate_with_context(
        self,
        system_prompt: str,
        context: str,
        task: str,
        temperature: Optional[float] = None,
        task_type: str = "default",
    ) -> str:
        user_prompt = f"""Contexto do documento:
{context}

Tarefa:
{task}"""
        return self.generate(
            system_prompt, user_prompt, temperature, task_type=task_type
        )


def get_llm_service(
    provider: Optional[str] = None,
    model: Optional[str] = None,
    complexity: Optional[TaskComplexity] = None,
) -> LLMService:
    return LLMService(provider, model, complexity)


def get_optimal_model_for_task(task_type: str) -> tuple[str, str]:
    complexity = TASK_COMPLEXITY_MAP.get(task_type, "medium")

    if complexity == "simple":
        return "MiniMax-M2.5", "MiniMax-M2.5 (tarefas simples - free)"
    elif complexity == "complex":
        return (
            settings.OPENAI_MODEL_COMPLEX,
            f"{settings.OPENAI_MODEL_COMPLEX} (tarefas complexas)",
        )
    else:
        return settings.OPENAI_MODEL, f"{settings.OPENAI_MODEL} (tarefas médias)"


def get_task_complexity(task_type: str) -> TaskComplexity:
    return TASK_COMPLEXITY_MAP.get(task_type, "medium")

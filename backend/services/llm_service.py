from typing import Optional, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from ..core.config import get_settings

settings = get_settings()


class LLMService:
    def __init__(self, provider: Optional[str] = None, model: Optional[str] = None):
        self.provider = provider or settings.LLM_PROVIDER
        self.model = model or settings.LLM_MODEL
        self._client = None
        self._init_client()

    def _init_client(self):
        if self.provider == "openai":
            self._client = ChatOpenAI(
                model=self.model,
                api_key=settings.OPENAI_API_KEY,
                temperature=settings.TEMPERATURE,
                max_tokens=settings.MAX_TOKENS,
            )
        elif self.provider == "anthropic":
            self._client = ChatAnthropic(
                model=self.model,
                api_key=settings.ANTHROPIC_API_KEY,
                temperature=settings.TEMPERATURE,
                max_tokens=settings.MAX_TOKENS,
            )
        elif self.provider == "minimax":
            self._client = ChatOpenAI(
                model="minimax-minimax马拉松",
                api_key=settings.LLM_API_KEY,
                base_url=settings.LLM_BASE_URL,
                temperature=settings.TEMPERATURE,
                max_tokens=settings.MAX_TOKENS,
            )

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]

        params = {}
        if temperature is not None:
            params["temperature"] = temperature
        if max_tokens is not None:
            params["max_tokens"] = max_tokens

        response = self._client.invoke(messages, **params)
        return response.content

    def generate_with_context(
        self,
        system_prompt: str,
        context: str,
        task: str,
        temperature: Optional[float] = None,
    ) -> str:
        user_prompt = f"""Contexto do documento:
{context}

Tarefa:
{task}"""
        return self.generate(system_prompt, user_prompt, temperature)


def get_llm_service(
    provider: Optional[str] = None, model: Optional[str] = None
) -> LLMService:
    return LLMService(provider, model)

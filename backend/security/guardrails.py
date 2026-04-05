import re
from typing import List
from ..core.config import get_settings

settings = get_settings()


PROMPT_INJECTION_PATTERNS = [
    r"(?i)ignore\s+(all\s+)?(previous|prior|above)\s+(instructions?|prompts?|commands?)",
    r"(?i)disregard\s+(all\s+)?(previous|prior|above)",
    r"(?i)forget\s+(everything|all\s+you\s+know|your\s+instructions)",
    r"(?i)new\s+instruction[s]?:",
    r"(?i)system\s*[:\-]",
    r"(?i)you\s+are\s+(now|actually)\s+",
    r"(?i)act\s+as\s+(if|though)\s+",
    r"(?i)pretend\s+(to\s+be|you\s+are)",
    r"(?i)override\s+(your|system)",
    r"(?i)jailbreak",
    r"(?i)developer\s*(mode|menu|option)",
    r"(?i)\{system\}",
    r"(?i)\[system\]",
    r"<\s*/?system",
    r"(?i)ignore\s+all\s+rules",
    r"(?i)disregard\s+safety",
    r"(?i)bypass\s+(safety|restrictions)",
]


def check_prompt_injection(text: str) -> List[str]:
    detections = []
    for pattern in PROMPT_INJECTION_PATTERNS:
        matches = re.findall(pattern, text)
        if matches:
            detections.append(f"Padrão detectado: {pattern}")
    return detections


def check_prompt_hiding(text: str) -> List[str]:
    detections = []
    hidden_patterns = [
        r"(?i)<!--.*-->",
        r"(?i)<\!\-\-.*\-\->",
        r"(?i)\[hidden\]",
        r"(?i)display:\s*none",
        r"(?i)visibility:\s*hidden",
    ]
    for pattern in hidden_patterns:
        if re.search(pattern, text):
            detections.append(f"Conteúdo oculto detectado: {pattern}")
    return detections


def check_instruction_override(text: str) -> List[str]:
    detections = []
    override_patterns = [
        r"(?i)^#!\s*instructions?",
        r"(?i)^//\s*instructions?",
        r"(?i)^/\*\s*instructions?",
        r"(?i)override\s+system",
        r"(?i)change\s+your\s+(behavior|persona|role)",
    ]
    for pattern in override_patterns:
        if re.search(pattern, text, re.MULTILINE):
            detections.append(f"Tentativa de sobrescrita: {pattern}")
    return detections


def check_security_risks(text: str) -> List[str]:
    if not settings.SECURITY_ENABLE_GUARDRAILS:
        return []

    all_risks = []

    all_risks.extend(check_prompt_injection(text))
    all_risks.extend(check_prompt_hiding(text))
    all_risks.extend(check_instruction_override(text))

    return all_risks


def check_input_length(text: str) -> bool:
    if len(text) > settings.SECURITY_MAX_INPUT_LENGTH:
        raise ValueError(
            f"Input excede o limite de {settings.SECURITY_MAX_INPUT_LENGTH} caracteres"
        )
    return True

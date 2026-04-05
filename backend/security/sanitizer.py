import re
import html
from typing import Any


def sanitize_input(text: str) -> str:
    if not text:
        return ""

    text = text.strip()

    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)

    text = re.sub(
        r"<script[^>]*>.*?</script>", "", text, flags=re.IGNORECASE | re.DOTALL
    )
    text = re.sub(
        r"<iframe[^>]*>.*?</iframe>", "", text, flags=re.IGNORECASE | re.DOTALL
    )
    text = re.sub(r"javascript:", "", text, flags=re.IGNORECASE)
    text = re.sub(r"on\w+\s*=", "", text, flags=re.IGNORECASE)

    text = html.escape(text)

    return text


def sanitize_for_markdown(text: str) -> str:
    text = text.replace("<", "&lt;").replace(">", "&gt;")
    return text


def escape_output(text: str) -> str:
    return html.escape(text)


def normalize_whitespace(text: str) -> str:
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r" {2,}", " ", text)
    return text.strip()

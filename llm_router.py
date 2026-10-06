"""
Local LLM helper: Ollama only (default gemma3:1b).
"""

from __future__ import annotations

import os
from typing import Any


def get_chat_model():
    """Return (ChatOllama, provider_name)."""
    from langchain_ollama import ChatOllama

    model = os.getenv("OLLAMA_MODEL", "gemma3:1b")
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    llm = ChatOllama(model=model, temperature=0.1, base_url=base_url)
    return llm, "ollama"


def invoke_llm(prompt_value: Any) -> tuple[str, str]:
    """Invoke Ollama. Returns (text, provider_used)."""
    llm, name = get_chat_model()
    result = llm.invoke(prompt_value)
    text = result.content if hasattr(result, "content") else str(result)
    return (text or "").strip(), name

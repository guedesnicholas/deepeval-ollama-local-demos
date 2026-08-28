"""
Configuração do modelo juiz usado nas demos — Ollama local por padrão,
no mesmo estilo do chatbot.py.

Variáveis de ambiente:
    JUIZ_PROVIDER   ollama (padrão) | gemini
    JUIZ_MODEL      nome do modelo juiz (padrões: llama3.2:3b / gemini-2.0-flash)
    OLLAMA_URL      URL do Ollama (padrão: http://localhost:11434)
    GEMINI_API_KEY  chave do Google AI Studio (só se JUIZ_PROVIDER=gemini)
"""

import os


def obter_juiz():
    provider = os.getenv("JUIZ_PROVIDER", "ollama").lower()

    if provider == "gemini":
        from deepeval.models import GeminiModel  # requer: pip install google-genai

        return GeminiModel(
            model=os.getenv("JUIZ_MODEL", "gemini-2.0-flash"),
            api_key=os.getenv("GEMINI_API_KEY"),
        )

    from deepeval.models import OllamaModel  # requer: pip install ollama

    return OllamaModel(
        model=os.getenv("JUIZ_MODEL", "llama3.1:latest"),
        base_url=os.getenv("OLLAMA_URL", "http://localhost:11434"),
        temperature=0
    )

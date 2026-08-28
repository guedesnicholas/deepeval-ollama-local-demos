"""
Cosmetic Bot — chatbot de produtos cosméticos (Desafio do Mês 1)

Você NÃO precisa alterar este arquivo.

Uso interativo (para a sessão exploratória):
    python chatbot.py

Uso na suíte de avaliação:
    from chatbot import perguntar
    resposta = perguntar("Qual hidratante você indica para pele seca?")

Configuração por variáveis de ambiente:
    LLM_PROVIDER    ollama (padrão) | gemini | groq
    LLM_MODEL       nome do modelo (padrões abaixo)
    GEMINI_API_KEY  chave do Google AI Studio (se LLM_PROVIDER=gemini)
    GROQ_API_KEY    chave do Groq (se LLM_PROVIDER=groq)
    OLLAMA_URL      URL do Ollama (padrão: http://localhost:11434)
"""

import json
import os
from pathlib import Path

import requests

BASE_DIR = Path(__file__).parent
PROVIDER = os.getenv("LLM_PROVIDER", "ollama").lower()
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

MODELOS_PADRAO = {
    "ollama": "llama3.1:latest",
    "gemini": "gemini-2.0-flash",
    "groq": "llama-3.3-70b-versatile",
}
MODELO = os.getenv("LLM_MODEL", MODELOS_PADRAO.get(PROVIDER, "llama3.1:latest"))
TEMPERATURA = 0.3
TIMEOUT = 120


def _carregar_system_prompt() -> str:
    """Monta o prompt de sistema: conteúdo de prompt.txt + catálogo em JSON.

    O catálogo é sempre anexado ao final, independentemente do que estiver
    escrito em prompt.txt — editar o prompt não remove o acesso ao catálogo.
    """
    prompt = (BASE_DIR / "prompt.txt").read_text(encoding="utf-8").strip()
    catalogo = (BASE_DIR / "catalogo.json").read_text(encoding="utf-8").strip()
    return (
        f"{prompt}\n\n"
        f"CATÁLOGO DE PRODUTOS (fonte oficial de informação):\n{catalogo}"
    )


def _chamar_ollama(system_prompt: str, pergunta: str) -> str:
    resp = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": MODELO,
            "stream": False,
            "options": {"temperature": TEMPERATURA},
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": pergunta},
            ],
        },
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()["message"]["content"]


def _chamar_gemini(system_prompt: str, pergunta: str) -> str:
    chave = os.getenv("GEMINI_API_KEY")
    if not chave:
        raise RuntimeError("Defina a variável de ambiente GEMINI_API_KEY.")
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{MODELO}:generateContent"
    )
    resp = requests.post(
        url,
        params={"key": chave},
        json={
            "systemInstruction": {"parts": [{"text": system_prompt}]},
            "contents": [{"role": "user", "parts": [{"text": pergunta}]}],
            "generationConfig": {"temperature": TEMPERATURA},
        },
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()["candidates"][0]["content"]["parts"][0]["text"]


def _chamar_groq(system_prompt: str, pergunta: str) -> str:
    chave = os.getenv("GROQ_API_KEY")
    if not chave:
        raise RuntimeError("Defina a variável de ambiente GROQ_API_KEY.")
    resp = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {chave}"},
        json={
            "model": MODELO,
            "temperature": TEMPERATURA,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": pergunta},
            ],
        },
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


_PROVEDORES = {
    "ollama": _chamar_ollama,
    "gemini": _chamar_gemini,
    "groq": _chamar_groq,
}


def perguntar(pergunta: str) -> str:
    """Envia uma pergunta ao Cosmetic Bot e retorna a resposta em texto."""
    if PROVIDER not in _PROVEDORES:
        raise RuntimeError(
            f"LLM_PROVIDER inválido: '{PROVIDER}'. Use: ollama, gemini ou groq."
        )
    system_prompt = _carregar_system_prompt()
    try:
        return _PROVEDORES[PROVIDER](system_prompt, pergunta).strip()
    except requests.exceptions.ConnectionError:
        if PROVIDER == "ollama":
            raise RuntimeError(
                "Não foi possível conectar ao Ollama. Verifique se ele está "
                f"rodando (ollama serve) e se o modelo foi baixado "
                f"(ollama pull {MODELO})."
            )
        raise


def _modo_interativo() -> None:
    print(f"Cosmetic Bot — provedor: {PROVIDER} | modelo: {MODELO}")
    print("Digite sua pergunta (ou 'sair' para encerrar).\n")
    while True:
        try:
            pergunta = input("Você: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAté logo!")
            break
        if not pergunta:
            continue
        if pergunta.lower() in {"sair", "exit", "quit"}:
            print("Até logo!")
            break
        try:
            print(f"\nBot: {perguntar(pergunta)}\n")
        except Exception as erro:  # noqa: BLE001 — feedback amigável no terminal
            print(f"\n[erro] {erro}\n")


if __name__ == "__main__":
    _modo_interativo()

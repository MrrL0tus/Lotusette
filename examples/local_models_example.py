"""Exemple d'utilisation du provider LLM local.

Lotusette parle à un serveur exposant l'API `/v1/chat/completions` d'OpenAI.
llama.cpp, Ollama et vLLM conviennent tous les trois.

Démarrer le serveur avant de lancer ce script :

    llama-server -hf mistralai/Ministral-3-3B-Instruct-2512-GGUF:Q4_K_M \\
        -c 8192 --port 8080 --host 127.0.0.1

Puis :

    python examples/local_models_example.py

Voir docs/MODELS.md pour le choix du modèle selon la machine.
"""

import asyncio
import os
import time

from lotusette.core.llm import LLMFactory

BASE_URL = os.environ.get("LOCAL_LLM_BASE_URL", "http://localhost:8080/v1")
# llama.cpp ignore ce champ et sert le modèle chargé au démarrage. Ollama et
# vLLM s'en servent pour choisir le modèle.
MODEL = os.environ.get("LOCAL_LLM_MODEL", "local")


def build_provider(temperature: float = 0.7, max_tokens: int = 200):
    """Create a provider pointing at the local inference server."""
    return LLMFactory.create_provider(
        provider_name="local",
        model=MODEL,
        temperature=temperature,
        max_tokens=max_tokens,
        base_url=BASE_URL,
        # Aucune clé n'est requise, mais l'en-tête doit être présent.
        api_key="EMPTY",
    )


async def exemple_simple():
    """Génération classique : on attend la réponse complète."""
    print("=" * 70)
    print("1. Génération simple")
    print("=" * 70)

    llm = build_provider()
    messages = [
        llm.create_message("system", "Tu es un assistant IA amical et serviable."),
        llm.create_message("user", "Explique-moi en une phrase ce qu'est l'IA."),
    ]

    started = time.perf_counter()
    response = await llm.generate(messages)
    elapsed = time.perf_counter() - started

    print(f"\nRéponse : {response.content}")
    print(f"Modèle servi : {response.model}")
    if response.tokens_used:
        print(f"Tokens : {response.tokens_used}")
    print(f"Durée : {elapsed:.1f} s")


async def exemple_streaming():
    """Génération en flux : le texte s'affiche au fil de la génération.

    C'est le mode utilisé par le CLI. Sur un modèle local, il fait toute la
    différence : la première parole arrive en quelques centaines de
    millisecondes au lieu d'attendre la réponse entière.
    """
    print("\n" + "=" * 70)
    print("2. Génération en flux")
    print("=" * 70)

    llm = build_provider(max_tokens=300)
    messages = [
        llm.create_message("system", "Tu es un assistant IA amical et serviable."),
        llm.create_message("user", "Raconte-moi une courte histoire sur un robot."),
    ]

    print()
    started = time.perf_counter()
    first_token_at = None
    chunks = 0

    async for chunk in llm.generate_stream(messages):
        if first_token_at is None:
            first_token_at = time.perf_counter()
        chunks += 1
        print(chunk, end="", flush=True)

    elapsed = time.perf_counter() - started
    print("\n")
    if first_token_at is not None:
        print(f"Premier token : {(first_token_at - started) * 1000:.0f} ms")
        print(f"Durée totale  : {elapsed:.1f} s (~{chunks / elapsed:.1f} tok/s)")


async def main():
    """Run both examples."""
    print(f"Serveur : {BASE_URL}")
    print(f"Modèle  : {MODEL}\n")

    try:
        await exemple_simple()
        await exemple_streaming()
    except RuntimeError as error:
        # Le provider produit déjà un message actionnable.
        print(f"\n{error}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))

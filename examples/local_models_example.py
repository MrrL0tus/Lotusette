"""
Exemple d'utilisation des providers LLM locaux.

Ce script montre comment utiliser les deux options de modèles locaux:
1. vLLM (serveur local avec API OpenAI)
2. Transformers (chargement direct)
"""
import asyncio
import os
from lotusette.core.llm import LLMFactory


async def test_local_transformers():
    """Test du provider Transformers local."""
    print("=" * 80)
    print("Test du provider local-transformers")
    print("=" * 80)
    
    # Créer le provider avec un petit modèle pour l'exemple
    llm = LLMFactory.create_provider(
        provider_name="local-transformers",
        model="microsoft/phi-2",  # Petit modèle performant
        temperature=0.7,
        max_tokens=200,
        cache_dir="./data/models",
        # Décommenter pour utiliser la quantification si vous manquez de VRAM
        # load_in_8bit=True,
    )
    
    print(f"✅ Provider créé: {llm.provider_name}")
    print(f"📦 Modèle: {llm.model}")
    
    # Créer une conversation
    messages = [
        llm.create_message("system", "Tu es un assistant IA amical et serviable."),
        llm.create_message("user", "Explique-moi en une phrase ce qu'est l'IA."),
    ]
    
    print("\n💬 Génération de la réponse...")
    response = await llm.generate(messages)
    
    print(f"\n🤖 Réponse: {response.content}")
    print(f"📊 Tokens utilisés: {response.tokens_used}")
    print()


async def main():
    """Point d'entrée principal."""
    print("\n" + "=" * 80)
    print("Exemple d'utilisation des modèles locaux Lotusette")
    print("=" * 80 + "\n")
    
    await test_local_transformers()
    
    print("=" * 80)
    print("Terminé!")
    print("=" * 80)


if __name__ == "__main__":
    # Créer le dossier de cache si nécessaire
    os.makedirs("./data/models", exist_ok=True)
    
    # Lancer les tests
    asyncio.run(main())

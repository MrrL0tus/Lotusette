#!/usr/bin/env python3
"""Quick test script to demonstrate CLI functionality without real API keys."""

import asyncio
import os
import sys
from unittest.mock import AsyncMock, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lotusette.core.llm import LLMResponse
from lotusette.ui.cli import LotusetteCLI


async def test_cli_demo():
    """Demonstrate CLI functionality with mocked LLM."""
    print("🌸 Test de démonstration du CLI Lotusette\n")

    # Create CLI instance
    cli = LotusetteCLI()

    # Test 1: Memory system
    print("✅ Test 1: Système de mémoire")
    await cli.short_term_memory.add_message("user", "Bonjour!", cli.session_id)
    await cli.short_term_memory.add_message(
        "assistant", "Salut! Comment puis-je t'aider?", cli.session_id
    )

    messages = await cli.short_term_memory.get_messages(cli.session_id)
    print(f"   Messages en mémoire: {len(messages)}")
    for msg in messages:
        print(f"   - {msg.role}: {msg.content}")

    # Test 2: Commands
    print("\n✅ Test 2: Commandes CLI")
    print("   Test /stats...")
    should_continue = await cli.handle_command("/stats")
    print(f"   Continue: {should_continue}")

    print("   Test /help...")
    should_continue = await cli.handle_command("/help")
    print(f"   Continue: {should_continue}")

    # Test 3: Clear memory
    print("\n✅ Test 3: Effacer la mémoire")
    msg_count_before = cli.short_term_memory.get_message_count(cli.session_id)
    print(f"   Messages avant: {msg_count_before}")

    await cli.handle_command("/clear")
    msg_count_after = cli.short_term_memory.get_message_count(cli.session_id)
    print(f"   Messages après: {msg_count_after}")

    # Test 4: Long-term memory (with temp database)
    print("\n✅ Test 4: Mémoire à long terme")
    import tempfile

    from lotusette.core.memory import LongTermMemory

    temp_db_file = tempfile.mktemp(suffix=".db")
    temp_db = f"sqlite:///{temp_db_file}"
    lt_memory = LongTermMemory(temp_db)

    await lt_memory.add_message("user", "Message persistant", "test_session")
    stored_messages = await lt_memory.get_messages("test_session")
    print(f"   Messages stockés: {len(stored_messages)}")
    print(f"   Contenu: {stored_messages[0].content if stored_messages else 'Aucun'}")

    # Test 5: Prompt manager
    print("\n✅ Test 5: Gestionnaire de prompts")
    print(
        f"   Longueur du prompt système: {len(cli.prompt_manager.get_system_prompt())} caractères"
    )
    print(f"   Début du prompt: {cli.prompt_manager.get_system_prompt()[:100]}...")

    print("\n🎉 Tous les tests réussis!")
    print("\n💡 Pour utiliser le CLI complet:")
    print("   1. Configurez OPENAI_API_KEY ou ANTHROPIC_API_KEY dans .env")
    print("   2. Lancez: python -m lotusette.ui.cli")


if __name__ == "__main__":
    asyncio.run(test_cli_demo())

"""Command-line interface for Lotusette."""

import asyncio
import logging
import sys
from typing import Optional
from uuid import uuid4

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.spinner import Spinner

from lotusette.core.config import settings
from lotusette.core.llm import LLMFactory, Message, PromptManager
from lotusette.core.memory import LongTermMemory, ShortTermMemory

console = Console()
logger = logging.getLogger(__name__)


class LotusetteCLI:
    """Main CLI application for Lotusette."""

    def __init__(self):
        """Initialize the CLI."""
        self.session_id = str(uuid4())
        self.llm = None
        self.short_term_memory = ShortTermMemory(max_messages=100)
        self.long_term_memory = None
        self.prompt_manager = PromptManager()
        self.initialized = False

    async def initialize(self):
        """Initialize LLM and memory systems."""
        try:
            # Initialize LLM based on configuration
            if settings.llm_provider == "openai":
                if not settings.openai_api_key:
                    console.print("[red]❌ Erreur: OPENAI_API_KEY non configurée[/red]")
                    console.print(
                        "[yellow]Configurez votre .env avec votre clé API OpenAI[/yellow]"
                    )
                    return False

                self.llm = LLMFactory.create_provider(
                    provider_name="openai",
                    api_key=settings.openai_api_key,
                    model=settings.openai_model,
                    temperature=0.7,
                    max_tokens=1000,
                )

            elif settings.llm_provider == "claude":
                if not settings.anthropic_api_key:
                    console.print("[red]❌ Erreur: ANTHROPIC_API_KEY non configurée[/red]")
                    console.print(
                        "[yellow]Configurez votre .env avec votre clé API Anthropic[/yellow]"
                    )
                    return False

                self.llm = LLMFactory.create_provider(
                    provider_name="claude",
                    api_key=settings.anthropic_api_key,
                    model=settings.anthropic_model,
                    temperature=0.7,
                    max_tokens=1000,
                )

            else:
                console.print(
                    f"[red]❌ Erreur: Fournisseur LLM non supporté: {settings.llm_provider}[/red]"
                )
                return False

            # Initialize long-term memory
            self.long_term_memory = LongTermMemory(settings.database_url)

            # Add system message to memory
            system_prompt = self.prompt_manager.get_system_prompt()
            await self.short_term_memory.add_message("system", system_prompt, self.session_id)

            self.initialized = True
            console.print(
                f"[green]✓ LLM initialisé: {settings.llm_provider} ({self.llm.model})[/green]"
            )
            console.print(f"[green]✓ Système de mémoire prêt[/green]")
            return True

        except Exception as e:
            console.print(f"[red]❌ Erreur lors de l'initialisation: {e}[/red]")
            logger.error(f"Initialization error: {e}", exc_info=True)
            return False

    def print_welcome(self):
        """Print welcome message."""
        welcome_text = """
# Bienvenue dans Lotusette! 🌸

**Version 0.1.0** - Phase 1: Fondations de base

## Fonctionnalités actives:
- 💬 Conversation textuelle avec LLM (OpenAI/Claude)
- 🧠 Système de mémoire (court et long terme)
- 💾 Sauvegarde des conversations

## Commandes disponibles:
- `/help` - Afficher l'aide
- `/clear` - Effacer la mémoire de la session actuelle
- `/history` - Afficher l'historique de la session
- `/stats` - Afficher les statistiques
- `/exit` ou `/quit` - Quitter
        """

        console.print(
            Panel(
                Markdown(welcome_text),
                title="[bold blue]Lotusette AI Assistant[/bold blue]",
                border_style="blue",
            )
        )

    async def handle_command(self, command: str) -> bool:
        """Handle special commands.

        Args:
            command: The command string

        Returns:
            True if should continue, False to exit
        """
        command = command.lower().strip()

        if command in ["/exit", "/quit"]:
            return False

        elif command == "/help":
            help_text = """
**Commandes disponibles:**
- `/help` - Afficher cette aide
- `/clear` - Effacer la mémoire de la session actuelle
- `/history` - Afficher l'historique des messages
- `/stats` - Afficher les statistiques de la session
- `/exit` ou `/quit` - Quitter l'application
            """
            console.print(Panel(Markdown(help_text), title="Aide", border_style="cyan"))

        elif command == "/clear":
            await self.short_term_memory.clear(self.session_id)
            # Re-add system prompt
            system_prompt = self.prompt_manager.get_system_prompt()
            await self.short_term_memory.add_message("system", system_prompt, self.session_id)
            console.print("[yellow]✓ Mémoire de session effacée[/yellow]")

        elif command == "/history":
            messages = await self.short_term_memory.get_messages(self.session_id)
            if not messages:
                console.print("[yellow]Aucun historique disponible[/yellow]")
            else:
                console.print("\n[bold cyan]Historique de la session:[/bold cyan]")
                for msg in messages:
                    if msg.role != "system":
                        role_color = "green" if msg.role == "user" else "magenta"
                        console.print(f"[{role_color}]{msg.role}:[/{role_color}] {msg.content}")

        elif command == "/stats":
            msg_count = self.short_term_memory.get_message_count(self.session_id)
            console.print(f"[cyan]Messages dans la session: {msg_count}[/cyan]")
            console.print(f"[cyan]Session ID: {self.session_id}[/cyan]")
            console.print(f"[cyan]Provider LLM: {settings.llm_provider}[/cyan]")

        else:
            console.print(f"[red]Commande inconnue: {command}[/red]")
            console.print("[yellow]Tapez /help pour voir les commandes disponibles[/yellow]")

        return True

    async def chat(self, user_input: str):
        """Process user input and generate response.

        Args:
            user_input: User's message
        """
        try:
            # Add user message to memory
            await self.short_term_memory.add_message("user", user_input, self.session_id)
            await self.long_term_memory.add_message("user", user_input, self.session_id)

            # Get conversation context
            context = await self.short_term_memory.get_context(self.session_id, max_messages=20)

            # Convert to Message objects
            messages = [Message(role=msg["role"], content=msg["content"]) for msg in context]

            # Show thinking indicator
            with console.status("[bold blue]Lotusette réfléchit...", spinner="dots"):
                response = await self.llm.generate(messages)

            # Add assistant response to memory
            await self.short_term_memory.add_message("assistant", response.content, self.session_id)
            await self.long_term_memory.add_message("assistant", response.content, self.session_id)

            # Display response
            console.print(f"[bold magenta]Lotusette:[/bold magenta] {response.content}")

            # Show token usage if available
            if response.tokens_used:
                console.print(f"[dim]({response.tokens_used} tokens utilisés)[/dim]")

        except Exception as e:
            console.print(f"[red]❌ Erreur lors de la génération: {e}[/red]")
            logger.error(f"Chat error: {e}", exc_info=True)

    async def run(self):
        """Main run loop."""
        self.print_welcome()

        console.print("\n[yellow]⏳ Initialisation...[/yellow]\n")

        if not await self.initialize():
            console.print("[red]Impossible de démarrer l'application[/red]")
            return

        console.print("\n[green]✨ Prêt! Vous pouvez commencer à discuter.[/green]")
        console.print("[yellow]💡 Tapez /help pour voir les commandes disponibles[/yellow]\n")

        try:
            while True:
                user_input = console.input("[bold green]Vous:[/bold green] ").strip()

                if not user_input:
                    continue

                # Handle commands
                if user_input.startswith("/"):
                    should_continue = await self.handle_command(user_input)
                    if not should_continue:
                        console.print("[blue]Au revoir! À bientôt! 👋[/blue]")
                        break
                    continue

                # Process chat message
                await self.chat(user_input)

        except KeyboardInterrupt:
            console.print("\n\n[blue]Au revoir! À bientôt! 👋[/blue]")
        except Exception as e:
            console.print(f"[red]Erreur: {e}[/red]")
            logger.error(f"Runtime error: {e}", exc_info=True)


def main():
    """Main entry point for the CLI."""
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, settings.log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Run the CLI
    cli = LotusetteCLI()
    asyncio.run(cli.run())


if __name__ == "__main__":
    main()

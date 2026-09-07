"""Command-line interface for Lotusette."""

import asyncio
import contextlib
import logging
import signal
import time
from uuid import uuid4

from rich.console import Console
from rich.live import Live
from rich.logging import RichHandler
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

from lotusette.core.config import ensure_directories, settings
from lotusette.core.llm import LLMFactory, Message, PromptManager
from lotusette.core.llm.factory import LOCAL_PROVIDER_ALIASES
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

    def _build_llm(self):
        """Create the LLM provider from the configuration.

        Returns:
            A provider instance, or None if the configuration is incomplete.
            Le message d'erreur est affiché ici, l'appelant se contente
            d'interrompre le démarrage.
        """
        provider = settings.llm_provider.lower()

        if provider == "openai":
            if not settings.openai_api_key:
                console.print("[red]❌ Erreur: OPENAI_API_KEY non configurée[/red]")
                console.print("[yellow]Configurez votre .env avec votre clé API OpenAI[/yellow]")
                return None

            return LLMFactory.create_provider(
                provider_name="openai",
                api_key=settings.openai_api_key,
                model=settings.openai_model,
                temperature=settings.llm_temperature,
                max_tokens=settings.llm_max_tokens,
            )

        if provider == "claude":
            if not settings.anthropic_api_key:
                console.print("[red]❌ Erreur: ANTHROPIC_API_KEY non configurée[/red]")
                console.print("[yellow]Configurez votre .env avec votre clé API Anthropic[/yellow]")
                return None

            return LLMFactory.create_provider(
                provider_name="claude",
                api_key=settings.anthropic_api_key,
                model=settings.anthropic_model,
                temperature=settings.llm_temperature,
                max_tokens=settings.llm_max_tokens,
            )

        if provider in LOCAL_PROVIDER_ALIASES:
            # Serveur local compatible OpenAI : aucune clé d'API requise.
            return LLMFactory.create_provider(
                provider_name=provider,
                api_key=settings.local_llm_api_key,
                model=settings.local_llm_model,
                temperature=settings.llm_temperature,
                max_tokens=settings.llm_max_tokens,
                base_url=settings.local_llm_base_url,
            )

        console.print(f"[red]❌ Erreur: Fournisseur LLM non supporté: {provider}[/red]")
        console.print(
            "[yellow]Valeurs possibles pour LLM_PROVIDER : local, openai, claude[/yellow]"
        )
        return None

    async def initialize(self):
        """Initialize LLM and memory systems."""
        try:
            ensure_directories()

            self.llm = self._build_llm()
            if self.llm is None:
                return False

            # Initialize long-term memory
            self.long_term_memory = LongTermMemory(settings.database_url)

            # Add system message to memory
            system_prompt = self.prompt_manager.get_system_prompt()
            await self.short_term_memory.add_message("system", system_prompt, self.session_id)

            self.initialized = True
            console.print(
                f"[green]✓ LLM initialisé: {self.llm.provider_name} ({self.llm.model})[/green]"
            )
            if self.llm.provider_name == "local":
                console.print(f"[green]✓ Serveur local: {settings.local_llm_base_url}[/green]")
            console.print("[green]✓ Système de mémoire prêt[/green]")
            return True

        except Exception as e:
            console.print(f"[red]❌ Erreur lors de l'initialisation: {e}[/red]")
            logger.error(f"Initialization error: {e}", exc_info=settings.debug)
            return False

    def print_welcome(self):
        """Print welcome message."""
        welcome_text = """
# Bienvenue dans Lotusette! 🌸

**Version 0.1.0** - Phase 1: Fondations de base

## Fonctionnalités actives:
- 💬 Conversation textuelle en local (llama.cpp / Ollama) ou via API
- ⚡ Réponse affichée au fil de la génération
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

**Pendant une réponse:** `Ctrl-C` interrompt la génération sans quitter.
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
                        line = Text()
                        line.append(f"{msg.role}: ", style=role_color)
                        line.append(msg.content)
                        console.print(line)

        elif command == "/stats":
            msg_count = self.short_term_memory.get_message_count(self.session_id)
            console.print(f"[cyan]Messages dans la session: {msg_count}[/cyan]")
            console.print(f"[cyan]Session ID: {self.session_id}[/cyan]")
            # /stats doit rester consultable même si l'initialisation a échoué.
            if self.llm is not None:
                console.print(f"[cyan]Provider LLM: {self.llm.provider_name}[/cyan]")
                console.print(f"[cyan]Modèle: {self.llm.model}[/cyan]")
            else:
                console.print("[yellow]Aucun provider LLM initialisé[/yellow]")

        else:
            console.print(f"[red]Commande inconnue: {command}[/red]")
            console.print("[yellow]Tapez /help pour voir les commandes disponibles[/yellow]")

        return True

    @staticmethod
    def _render_reply(content: str, done: bool = False) -> Text:
        """Render the assistant reply for the live display.

        Le contenu passe par ``Text.append`` et non par le balisage de rich :
        une réponse du modèle contenant des crochets ne doit pas être
        interprétée comme du balisage.
        """
        text = Text()
        text.append("Lotusette: ", style="bold magenta")
        text.append(content)
        if not done and not content:
            text.append("…", style="dim")
        return text

    @staticmethod
    @contextlib.contextmanager
    def _sigint_as_event(event: asyncio.Event):
        """Route Ctrl-C to an asyncio.Event for the duration of the block.

        Pendant la génération, Ctrl-C doit interrompre la réponse en cours et
        rendre la main à l'invite, sans quitter l'application. Un
        ``except KeyboardInterrupt`` ne convient pas : le signal est levé dans
        la boucle d'événements, pas dans la coroutine.
        """
        loop = asyncio.get_running_loop()

        try:
            loop.add_signal_handler(signal.SIGINT, event.set)
        except (NotImplementedError, RuntimeError):
            # Windows n'implémente pas add_signal_handler.
            previous = signal.getsignal(signal.SIGINT)

            def _handler(_signum, _frame):
                loop.call_soon_threadsafe(event.set)

            signal.signal(signal.SIGINT, _handler)
            try:
                yield
            finally:
                signal.signal(signal.SIGINT, previous)
            return

        try:
            yield
        finally:
            with contextlib.suppress(NotImplementedError, RuntimeError):
                loop.remove_signal_handler(signal.SIGINT)

    async def _stream_reply(self, messages) -> tuple[str, float | None, float, int, bool]:
        """Stream a reply and display it as it arrives.

        Returns:
            (content, time_to_first_token, total_elapsed, chunk_count, interrupted)
        """
        stop = asyncio.Event()
        chunks: list[str] = []
        first_token_at: float | None = None
        started = time.perf_counter()

        with self._sigint_as_event(stop):
            with Live(
                self._render_reply(""),
                console=console,
                refresh_per_second=12,
                transient=False,
            ) as live:
                try:
                    # aclosing garantit la fermeture du générateur si l'on sort
                    # de la boucle avant la fin du flux.
                    async with contextlib.aclosing(self.llm.generate_stream(messages)) as stream:
                        async for chunk in stream:
                            if stop.is_set():
                                break

                            if first_token_at is None:
                                first_token_at = time.perf_counter()

                            chunks.append(chunk)
                            live.update(self._render_reply("".join(chunks)))
                except BaseException:
                    # Ne pas laisser le gabarit d'attente à l'écran : l'appelant
                    # va afficher un message d'erreur à la place.
                    live.update(Text(""))
                    raise

                live.update(self._render_reply("".join(chunks), done=True))

        elapsed = time.perf_counter() - started
        ttft = (first_token_at - started) if first_token_at is not None else None
        return "".join(chunks), ttft, elapsed, len(chunks), stop.is_set()

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
            context = await self.short_term_memory.get_context(
                self.session_id, max_messages=settings.llm_context_messages
            )

            # Convert to Message objects
            messages = [Message(role=msg["role"], content=msg["content"]) for msg in context]

            content, ttft, elapsed, chunk_count, interrupted = await self._stream_reply(messages)

            if interrupted:
                console.print("[yellow]⏹ Génération interrompue[/yellow]")

            if not content:
                console.print("[yellow]Aucune réponse reçue du modèle[/yellow]")
                return

            # Add assistant response to memory. Une réponse interrompue est
            # conservée : elle fait partie de ce que l'utilisateur a lu.
            await self.short_term_memory.add_message("assistant", content, self.session_id)
            await self.long_term_memory.add_message("assistant", content, self.session_id)

            if ttft is not None:
                # Le débit est approximatif : la plupart des serveurs
                # compatibles OpenAI émettent un fragment par token, mais rien
                # ne le garantit.
                rate = chunk_count / elapsed if elapsed > 0 else 0
                console.print(
                    f"[dim]({ttft * 1000:.0f} ms jusqu'au premier token, "
                    f"{elapsed:.1f} s au total, ~{rate:.1f} tok/s)[/dim]"
                )

        except Exception as e:
            console.print(f"[red]❌ Erreur lors de la génération: {e}[/red]")
            logger.debug(f"Chat error: {e}", exc_info=True)

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

        except (KeyboardInterrupt, EOFError):
            console.print("\n\n[blue]Au revoir! À bientôt! 👋[/blue]")
        except Exception as e:
            console.print(f"[red]Erreur: {e}[/red]")
            logger.error(f"Runtime error: {e}", exc_info=settings.debug)


def main():
    """Main entry point for the CLI."""
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=console, rich_tracebacks=True, show_path=False)],
    )

    # Run the CLI
    cli = LotusetteCLI()
    asyncio.run(cli.run())


if __name__ == "__main__":
    main()

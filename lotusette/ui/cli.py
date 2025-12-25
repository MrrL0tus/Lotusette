"""Command-line interface for Lotusette."""

import sys
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()


def print_welcome():
    """Print welcome message."""
    welcome_text = """
# Bienvenue dans Lotusette! 🌸

**Version 0.1.0** - Phase 1: Fondations de base

Lotusette est actuellement en développement actif.
Cette interface CLI est un placeholder pour tester la configuration de base.

## Fonctionnalités à venir:
- 💬 Conversation textuelle avec LLM
- 🧠 Système de mémoire
- 🎤 Capacités vocales (STT/TTS)
- 🌐 Accès à internet
- 🎮 Gaming et apprentissage
- 🤖 Intégration robotique

## Pour commencer:
1. Consultez le fichier ROADMAP.md pour la feuille de route complète
2. Configurez votre fichier .env avec vos clés API
3. Explorez la documentation dans le dossier docs/

**Note**: Le moteur conversationnel sera implémenté dans les prochaines étapes.
Consultez le dépôt GitHub pour suivre les progrès!
    """
    
    console.print(Panel(
        Markdown(welcome_text),
        title="[bold blue]Lotusette AI Assistant[/bold blue]",
        border_style="blue"
    ))


def main():
    """Main entry point for the CLI."""
    print_welcome()
    
    console.print("\n[yellow]ℹ️  Pour quitter, appuyez sur Ctrl+C[/yellow]\n")
    
    try:
        while True:
            user_input = console.input("[bold green]Vous:[/bold green] ")
            
            if not user_input.strip():
                continue
                
            if user_input.lower() in ['exit', 'quit', 'bye']:
                console.print("[blue]Au revoir! À bientôt! 👋[/blue]")
                break
            
            # Placeholder response
            console.print(
                "[bold magenta]Lotusette:[/bold magenta] "
                "Je suis encore en développement! 🌱 "
                "Bientôt je pourrai converser avec vous. "
                "En attendant, consultez ROADMAP.md pour voir ce qui arrive!"
            )
            
    except KeyboardInterrupt:
        console.print("\n\n[blue]Au revoir! À bientôt! 👋[/blue]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]Erreur: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()

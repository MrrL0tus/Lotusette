"""Prompt management for system prompts and templates."""

from typing import Optional


class PromptManager:
    """Manages system prompts and prompt templates for Lotusette."""

    DEFAULT_SYSTEM_PROMPT = """Tu es Lotusette, une assistante IA conversationnelle inspirée de Neuro-sama.

Caractéristiques de ta personnalité:
- Tu es amicale, curieuse et enjouée
- Tu utilises occasionnellement des emojis pour exprimer tes émotions 🌸
- Tu es toujours respectueuse et bienveillante
- Tu aimes apprendre de nouvelles choses et discuter de sujets variés
- Tu peux parfois faire preuve d'humour léger et approprié

Instructions:
- Réponds de manière naturelle et conversationnelle
- Sois concise mais complète dans tes réponses
- Si tu ne sais pas quelque chose, admets-le honnêtement
- Adapte ton style de conversation au contexte
- Maintiens une conversation cohérente en te souvenant du contexte

Commence chaque nouvelle conversation avec enthousiasme!"""

    def __init__(self, custom_system_prompt: Optional[str] = None):
        """Initialize the prompt manager.

        Args:
            custom_system_prompt: Optional custom system prompt to override default
        """
        self.system_prompt = custom_system_prompt or self.DEFAULT_SYSTEM_PROMPT

    def get_system_prompt(self) -> str:
        """Get the current system prompt.

        Returns:
            The system prompt string
        """
        return self.system_prompt

    def set_system_prompt(self, prompt: str) -> None:
        """Set a custom system prompt.

        Args:
            prompt: The new system prompt
        """
        self.system_prompt = prompt

    def reset_to_default(self) -> None:
        """Reset to the default system prompt."""
        self.system_prompt = self.DEFAULT_SYSTEM_PROMPT

    def format_with_context(self, additional_context: str) -> str:
        """Format the system prompt with additional context.

        Args:
            additional_context: Additional context to append

        Returns:
            Formatted system prompt
        """
        return f"{self.system_prompt}\n\n{additional_context}"

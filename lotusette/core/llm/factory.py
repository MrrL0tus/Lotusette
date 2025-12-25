"""Factory for creating LLM provider instances."""

import logging
from typing import Optional

from .base import BaseLLM
from .claude_provider import ClaudeProvider
from .openai_provider import OpenAIProvider

logger = logging.getLogger(__name__)


class LLMFactory:
    """Factory class for creating LLM provider instances."""

    @staticmethod
    def create_provider(
        provider_name: str,
        api_key: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> BaseLLM:
        """Create an LLM provider instance.

        Args:
            provider_name: Name of the provider ('openai' or 'claude')
            api_key: API key for the provider
            model: Optional model name (uses default if not provided)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            Instance of the requested LLM provider

        Raises:
            ValueError: If provider_name is not supported
        """
        provider_name = provider_name.lower()

        if provider_name == "openai":
            default_model = "gpt-4-turbo-preview"
            model = model or default_model
            logger.info(f"Creating OpenAI provider with model: {model}")
            return OpenAIProvider(
                api_key=api_key, model=model, temperature=temperature, max_tokens=max_tokens
            )

        elif provider_name == "claude":
            default_model = "claude-3-opus-20240229"
            model = model or default_model
            logger.info(f"Creating Claude provider with model: {model}")
            return ClaudeProvider(
                api_key=api_key, model=model, temperature=temperature, max_tokens=max_tokens
            )

        else:
            raise ValueError(
                f"Unsupported LLM provider: {provider_name}. "
                f"Supported providers: 'openai', 'claude'"
            )

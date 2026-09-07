"""Factory for creating LLM provider instances."""

import logging

from .base import BaseLLM
from .claude_provider import ClaudeProvider
from .local_openai_provider import LocalOpenAIProvider
from .openai_provider import OpenAIProvider

logger = logging.getLogger(__name__)

# 'local-vllm' est l'ancien nom du provider local. Il reste accepté pour ne pas
# casser les configurations existantes.
LOCAL_PROVIDER_ALIASES = ("local", "local-vllm", "llamacpp", "ollama")

SUPPORTED_PROVIDERS = ("openai", "claude", *LOCAL_PROVIDER_ALIASES)


class LLMFactory:
    """Factory class for creating LLM provider instances."""

    @staticmethod
    def create_provider(
        provider_name: str,
        api_key: str = "",
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs,
    ) -> BaseLLM:
        """Create an LLM provider instance.

        Args:
            provider_name: 'local' (ou son alias 'local-vllm'), 'openai', 'claude'
            api_key: API key for the provider (facultative pour le provider local)
            model: Optional model name (uses default if not provided)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional provider-specific arguments

        Returns:
            Instance of the requested LLM provider

        Raises:
            ValueError: If provider_name is not supported
        """
        provider_name = provider_name.lower()

        if provider_name == "openai":
            model = model or "gpt-4-turbo-preview"
            logger.debug(f"Creating OpenAI provider with model: {model}")
            return OpenAIProvider(
                api_key=api_key, model=model, temperature=temperature, max_tokens=max_tokens
            )

        elif provider_name == "claude":
            model = model or "claude-3-opus-20240229"
            logger.debug(f"Creating Claude provider with model: {model}")
            return ClaudeProvider(
                api_key=api_key, model=model, temperature=temperature, max_tokens=max_tokens
            )

        elif provider_name in LOCAL_PROVIDER_ALIASES:
            # Serveur local exposant une API compatible OpenAI
            # (llama.cpp, Ollama, vLLM).
            if not model:
                raise ValueError("Model name is required for the local provider")

            base_url = kwargs.get("base_url", "http://localhost:8080/v1")
            logger.debug(f"Creating local LLM provider with model: {model}")
            logger.debug(f"Server URL: {base_url}")

            return LocalOpenAIProvider(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                base_url=base_url,
                api_key=api_key or "EMPTY",
            )

        else:
            raise ValueError(
                f"Unsupported LLM provider: {provider_name}. "
                f"Supported providers: {', '.join(repr(p) for p in SUPPORTED_PROVIDERS)}"
            )

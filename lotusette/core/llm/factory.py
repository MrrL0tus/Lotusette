"""Factory for creating LLM provider instances."""

import logging
from typing import Optional

from .base import BaseLLM
from .claude_provider import ClaudeProvider
from .openai_provider import OpenAIProvider
from .local_vllm_provider import LocalVLLMProvider
from .local_transformers_provider import LocalTransformersProvider

logger = logging.getLogger(__name__)


class LLMFactory:
    """Factory class for creating LLM provider instances."""

    @staticmethod
    def create_provider(
        provider_name: str,
        api_key: str = "",
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs,
    ) -> BaseLLM:
        """Create an LLM provider instance.

        Args:
            provider_name: Name of the provider ('openai', 'claude', 'local-vllm', 'local-transformers')
            api_key: API key for the provider (not required for local providers)
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

        elif provider_name == "local-vllm":
            # Provider pour serveur vLLM local (API compatible OpenAI)
            if not model:
                raise ValueError("Model name is required for local-vllm provider")
            
            base_url = kwargs.get("base_url", "http://localhost:8001/v1")
            logger.info(f"Creating local vLLM provider with model: {model}")
            logger.info(f"Server URL: {base_url}")
            
            return LocalVLLMProvider(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                base_url=base_url,
                api_key=api_key or "EMPTY",
            )

        elif provider_name == "local-transformers":
            # Provider pour modèles HuggingFace locaux via Transformers
            if not model:
                raise ValueError("Model name is required for local-transformers provider")
            
            device = kwargs.get("device", None)
            cache_dir = kwargs.get("cache_dir", None)
            load_in_8bit = kwargs.get("load_in_8bit", False)
            load_in_4bit = kwargs.get("load_in_4bit", False)
            
            logger.info(f"Creating local Transformers provider with model: {model}")
            
            return LocalTransformersProvider(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                device=device,
                cache_dir=cache_dir,
                load_in_8bit=load_in_8bit,
                load_in_4bit=load_in_4bit,
            )

        else:
            raise ValueError(
                f"Unsupported LLM provider: {provider_name}. "
                f"Supported providers: 'openai', 'claude', 'local-vllm', 'local-transformers'"
            )

"""Unit tests for LLM factory."""

import pytest

from lotusette.core.llm import ClaudeProvider, LLMFactory, OpenAIProvider


class TestLLMFactory:
    """Tests for LLM factory."""

    def test_create_openai_provider(self):
        """Test creating OpenAI provider."""
        provider = LLMFactory.create_provider(
            provider_name="openai", api_key="test-key", model="gpt-4-turbo-preview"
        )
        assert isinstance(provider, OpenAIProvider)
        assert provider.model == "gpt-4-turbo-preview"

    def test_create_claude_provider(self):
        """Test creating Claude provider."""
        provider = LLMFactory.create_provider(
            provider_name="claude", api_key="test-key", model="claude-3-opus-20240229"
        )
        assert isinstance(provider, ClaudeProvider)
        assert provider.model == "claude-3-opus-20240229"

    def test_case_insensitive_provider_name(self):
        """Test that provider names are case-insensitive."""
        provider1 = LLMFactory.create_provider("OPENAI", "key")
        provider2 = LLMFactory.create_provider("OpenAI", "key")
        provider3 = LLMFactory.create_provider("openai", "key")

        assert all(isinstance(p, OpenAIProvider) for p in [provider1, provider2, provider3])

    def test_invalid_provider_raises_error(self):
        """Test that invalid provider raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported LLM provider"):
            LLMFactory.create_provider("invalid_provider", "key")

    def test_default_models(self):
        """Test that default models are used when not specified."""
        openai_provider = LLMFactory.create_provider("openai", "key")
        assert openai_provider.model == "gpt-4-turbo-preview"

        claude_provider = LLMFactory.create_provider("claude", "key")
        assert claude_provider.model == "claude-3-opus-20240229"

    def test_custom_parameters(self):
        """Test creating provider with custom parameters."""
        provider = LLMFactory.create_provider(
            provider_name="openai", api_key="key", temperature=0.9, max_tokens=2000
        )
        assert provider.temperature == 0.9
        assert provider.max_tokens == 2000

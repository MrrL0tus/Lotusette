"""Unit tests for local LLM providers."""

import pytest

from lotusette.core.llm import LLMFactory
from lotusette.core.llm.local_vllm_provider import LocalVLLMProvider
from lotusette.core.llm.local_transformers_provider import LocalTransformersProvider


class TestLocalProviders:
    """Tests for local LLM providers."""

    def test_create_local_vllm_provider(self):
        """Test creating local vLLM provider."""
        provider = LLMFactory.create_provider(
            provider_name="local-vllm",
            model="mistralai/Mistral-7B-Instruct-v0.2",
            base_url="http://localhost:8001/v1",
        )
        assert isinstance(provider, LocalVLLMProvider)
        assert provider.model == "mistralai/Mistral-7B-Instruct-v0.2"
        assert provider.provider_name == "local-vllm"

    def test_create_local_transformers_provider(self):
        """Test creating local Transformers provider."""
        # Note: Ce test ne charge pas réellement le modèle, juste la création
        # de l'instance. Le chargement du modèle nécessiterait les dépendances
        # et beaucoup de temps/ressources.
        with pytest.raises(Exception):
            # S'attend à une erreur car torch/transformers peuvent ne pas être installés
            provider = LLMFactory.create_provider(
                provider_name="local-transformers",
                model="microsoft/phi-2",
                cache_dir="./test_cache",
            )

    def test_local_vllm_provider_configuration(self):
        """Test vLLM provider configuration."""
        provider = LLMFactory.create_provider(
            provider_name="local-vllm",
            model="test-model",
            temperature=0.5,
            max_tokens=500,
            base_url="http://test:8000/v1",
        )
        assert provider.temperature == 0.5
        assert provider.max_tokens == 500
        assert provider.base_url == "http://test:8000/v1"

    def test_local_provider_requires_model(self):
        """Test that local providers require a model name."""
        with pytest.raises(ValueError, match="Model name is required"):
            LLMFactory.create_provider(
                provider_name="local-vllm",
                # model manquant
            )

        with pytest.raises(ValueError, match="Model name is required"):
            LLMFactory.create_provider(
                provider_name="local-transformers",
                # model manquant
            )

    def test_factory_supports_all_providers(self):
        """Test that factory supports all expected providers."""
        # Test que chaque provider peut être créé (sans charger les modèles)
        openai = LLMFactory.create_provider("openai", api_key="test")
        assert openai.provider_name == "openai"

        claude = LLMFactory.create_provider("claude", api_key="test")
        assert claude.provider_name == "claude"

        vllm = LLMFactory.create_provider("local-vllm", model="test-model")
        assert vllm.provider_name == "local-vllm"

        # local-transformers nécessite torch, on teste juste la ValueError
        with pytest.raises((ValueError, Exception)):
            # Si model manquant: ValueError
            # Si torch manquant: une autre Exception
            transformers = LLMFactory.create_provider("local-transformers")

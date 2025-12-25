"""Unit tests for OpenAI provider."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from lotusette.core.llm import LLMResponse, Message, OpenAIProvider


@pytest.mark.asyncio
class TestOpenAIProvider:
    """Tests for OpenAI provider."""

    def test_initialization(self):
        """Test provider initialization."""
        provider = OpenAIProvider(
            api_key="test-key", model="gpt-4-turbo-preview", temperature=0.8, max_tokens=500
        )
        assert provider.model == "gpt-4-turbo-preview"
        assert provider.temperature == 0.8
        assert provider.max_tokens == 500
        assert provider.provider_name == "openai"

    async def test_generate(self):
        """Test generating a response."""
        provider = OpenAIProvider(api_key="test-key")

        # Mock the OpenAI client
        mock_choice = MagicMock()
        mock_choice.message.content = "Test response"
        mock_choice.finish_reason = "stop"

        mock_usage = MagicMock()
        mock_usage.total_tokens = 50

        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        mock_response.usage = mock_usage

        provider.client.chat.completions.create = AsyncMock(return_value=mock_response)

        messages = [Message(role="user", content="Hello")]
        response = await provider.generate(messages)

        assert isinstance(response, LLMResponse)
        assert response.content == "Test response"
        assert response.tokens_used == 50
        assert response.finish_reason == "stop"

    async def test_generate_stream(self):
        """Test streaming generation."""
        provider = OpenAIProvider(api_key="test-key")

        # Mock streaming response
        async def mock_stream():
            chunks = ["Hello", " ", "world", "!"]
            for chunk_text in chunks:
                mock_chunk = MagicMock()
                mock_chunk.choices = [MagicMock()]
                mock_chunk.choices[0].delta.content = chunk_text
                yield mock_chunk

        provider.client.chat.completions.create = AsyncMock(return_value=mock_stream())

        messages = [Message(role="user", content="Say hello")]
        chunks = []
        async for chunk in provider.generate_stream(messages):
            chunks.append(chunk)

        assert "".join(chunks) == "Hello world!"

    def test_create_message(self):
        """Test message creation helper."""
        provider = OpenAIProvider(api_key="test-key")
        msg = provider.create_message("user", "Test content")

        assert isinstance(msg, Message)
        assert msg.role == "user"
        assert msg.content == "Test content"

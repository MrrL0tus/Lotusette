"""Unit tests for Claude provider."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from lotusette.core.llm import ClaudeProvider, LLMResponse, Message


@pytest.mark.asyncio
class TestClaudeProvider:
    """Tests for Claude provider."""

    def test_initialization(self):
        """Test provider initialization."""
        provider = ClaudeProvider(
            api_key="test-key", model="claude-3-opus-20240229", temperature=0.8, max_tokens=500
        )
        assert provider.model == "claude-3-opus-20240229"
        assert provider.temperature == 0.8
        assert provider.max_tokens == 500
        assert provider.provider_name == "claude"

    async def test_generate(self):
        """Test generating a response."""
        provider = ClaudeProvider(api_key="test-key")

        # Mock the Anthropic client
        mock_content = MagicMock()
        mock_content.text = "Test response from Claude"

        mock_usage = MagicMock()
        mock_usage.input_tokens = 20
        mock_usage.output_tokens = 30

        mock_response = MagicMock()
        mock_response.content = [mock_content]
        mock_response.usage = mock_usage
        mock_response.stop_reason = "end_turn"

        provider.client.messages.create = AsyncMock(return_value=mock_response)

        messages = [
            Message(role="system", content="You are helpful"),
            Message(role="user", content="Hello"),
        ]
        response = await provider.generate(messages)

        assert isinstance(response, LLMResponse)
        assert response.content == "Test response from Claude"
        assert response.tokens_used == 50  # 20 + 30
        assert response.finish_reason == "end_turn"

    async def test_generate_with_system_message(self):
        """Test that system messages are handled separately."""
        provider = ClaudeProvider(api_key="test-key")

        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Response")]
        mock_response.usage = MagicMock(input_tokens=10, output_tokens=20)
        mock_response.stop_reason = "end_turn"

        provider.client.messages.create = AsyncMock(return_value=mock_response)

        messages = [
            Message(role="system", content="System prompt"),
            Message(role="user", content="Hello"),
        ]

        await provider.generate(messages)

        # Verify that create was called with system as a separate parameter
        call_kwargs = provider.client.messages.create.call_args.kwargs
        assert "system" in call_kwargs
        assert call_kwargs["system"] == "System prompt"
        # Verify that messages doesn't include system message
        assert all(m["role"] != "system" for m in call_kwargs["messages"])

    def test_create_message(self):
        """Test message creation helper."""
        provider = ClaudeProvider(api_key="test-key")
        msg = provider.create_message("assistant", "Test response")

        assert isinstance(msg, Message)
        assert msg.role == "assistant"
        assert msg.content == "Test response"

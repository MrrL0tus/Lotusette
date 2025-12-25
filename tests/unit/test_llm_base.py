"""Unit tests for LLM base classes."""

import pytest

from lotusette.core.llm import LLMResponse, Message


class TestMessage:
    """Tests for Message class."""

    def test_message_creation(self):
        """Test creating a message."""
        msg = Message(role="user", content="Hello")
        assert msg.role == "user"
        assert msg.content == "Hello"

    def test_message_to_dict(self):
        """Test converting message to dictionary."""
        msg = Message(role="assistant", content="Hi there!")
        msg_dict = msg.to_dict()
        assert msg_dict == {"role": "assistant", "content": "Hi there!"}

    def test_different_roles(self):
        """Test different message roles."""
        roles = ["system", "user", "assistant"]
        for role in roles:
            msg = Message(role=role, content="Test")
            assert msg.role == role


class TestLLMResponse:
    """Tests for LLMResponse class."""

    def test_response_creation(self):
        """Test creating an LLM response."""
        response = LLMResponse(
            content="Test content", model="test-model", tokens_used=100, finish_reason="stop"
        )
        assert response.content == "Test content"
        assert response.model == "test-model"
        assert response.tokens_used == 100
        assert response.finish_reason == "stop"

    def test_response_optional_fields(self):
        """Test response with optional fields."""
        response = LLMResponse(content="Test", model="test")
        assert response.content == "Test"
        assert response.model == "test"
        assert response.tokens_used is None
        assert response.finish_reason is None

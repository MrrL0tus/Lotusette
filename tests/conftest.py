"""Test fixtures and utilities."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from lotusette.core.llm import LLMResponse, Message


@pytest.fixture
def sample_messages():
    """Sample messages for testing."""
    return [
        Message(role="system", content="You are a helpful assistant."),
        Message(role="user", content="Hello!"),
        Message(role="assistant", content="Hi there! How can I help you?"),
    ]


@pytest.fixture
def mock_llm_response():
    """Mock LLM response."""
    return LLMResponse(
        content="This is a test response", model="test-model", tokens_used=50, finish_reason="stop"
    )


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client."""
    mock = AsyncMock()
    mock.chat.completions.create = AsyncMock()
    return mock


@pytest.fixture
def mock_anthropic_client():
    """Mock Anthropic client."""
    mock = AsyncMock()
    mock.messages.create = AsyncMock()
    return mock


@pytest.fixture
def temp_database_url(tmp_path):
    """Temporary database URL for testing."""
    db_path = tmp_path / "test.db"
    return f"sqlite:///{db_path}"

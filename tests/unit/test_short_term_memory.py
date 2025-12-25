"""Unit tests for short-term memory."""

from datetime import datetime

import pytest

from lotusette.core.memory import ConversationMessage, ShortTermMemory


@pytest.mark.asyncio
class TestShortTermMemory:
    """Tests for ShortTermMemory."""

    async def test_initialization(self):
        """Test memory initialization."""
        memory = ShortTermMemory(max_messages=50)
        assert memory.max_messages == 50

    async def test_add_message(self):
        """Test adding a message."""
        memory = ShortTermMemory()
        await memory.add_message("user", "Hello", session_id="test")

        messages = await memory.get_messages(session_id="test")
        assert len(messages) == 1
        assert messages[0].role == "user"
        assert messages[0].content == "Hello"
        assert messages[0].session_id == "test"

    async def test_get_messages_with_limit(self):
        """Test retrieving messages with limit."""
        memory = ShortTermMemory()

        # Add multiple messages
        for i in range(10):
            await memory.add_message("user", f"Message {i}", session_id="test")

        messages = await memory.get_messages(session_id="test", limit=5)
        assert len(messages) == 5
        # Should get the last 5 messages
        assert messages[0].content == "Message 5"
        assert messages[-1].content == "Message 9"

    async def test_session_filtering(self):
        """Test filtering by session ID."""
        memory = ShortTermMemory()

        await memory.add_message("user", "Session 1", session_id="session1")
        await memory.add_message("user", "Session 2", session_id="session2")
        await memory.add_message("user", "Another in Session 1", session_id="session1")

        session1_messages = await memory.get_messages(session_id="session1")
        assert len(session1_messages) == 2
        assert all(m.session_id == "session1" for m in session1_messages)

        session2_messages = await memory.get_messages(session_id="session2")
        assert len(session2_messages) == 1
        assert session2_messages[0].session_id == "session2"

    async def test_clear_all(self):
        """Test clearing all messages."""
        memory = ShortTermMemory()

        await memory.add_message("user", "Test 1")
        await memory.add_message("user", "Test 2")

        await memory.clear()

        messages = await memory.get_messages()
        assert len(messages) == 0

    async def test_clear_session(self):
        """Test clearing specific session."""
        memory = ShortTermMemory()

        await memory.add_message("user", "Session 1", session_id="session1")
        await memory.add_message("user", "Session 2", session_id="session2")

        await memory.clear(session_id="session1")

        messages = await memory.get_messages()
        assert len(messages) == 1
        assert messages[0].session_id == "session2"

    async def test_get_context(self):
        """Test getting context for LLM."""
        memory = ShortTermMemory()

        await memory.add_message("system", "System prompt", session_id="test")
        await memory.add_message("user", "Hello", session_id="test")
        await memory.add_message("assistant", "Hi there!", session_id="test")

        context = await memory.get_context(session_id="test")

        assert len(context) == 3
        assert context[0] == {"role": "system", "content": "System prompt"}
        assert context[1] == {"role": "user", "content": "Hello"}
        assert context[2] == {"role": "assistant", "content": "Hi there!"}

    async def test_max_messages_limit(self):
        """Test that max_messages limit is enforced."""
        memory = ShortTermMemory(max_messages=5)

        # Add more than max
        for i in range(10):
            await memory.add_message("user", f"Message {i}")

        messages = await memory.get_messages()
        assert len(messages) == 5
        # Should keep the last 5
        assert messages[0].content == "Message 5"
        assert messages[-1].content == "Message 9"

    async def test_get_message_count(self):
        """Test getting message count."""
        memory = ShortTermMemory()

        await memory.add_message("user", "Test 1", session_id="session1")
        await memory.add_message("user", "Test 2", session_id="session1")
        await memory.add_message("user", "Test 3", session_id="session2")

        assert memory.get_message_count() == 3
        assert memory.get_message_count(session_id="session1") == 2
        assert memory.get_message_count(session_id="session2") == 1

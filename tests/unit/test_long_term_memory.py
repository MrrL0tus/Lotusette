"""Unit tests for long-term memory."""

import pytest

from lotusette.core.memory import ConversationMessage, LongTermMemory


@pytest.mark.asyncio
class TestLongTermMemory:
    """Tests for LongTermMemory."""

    async def test_initialization(self, temp_database_url):
        """Test memory initialization with database."""
        memory = LongTermMemory(temp_database_url)
        assert memory.database_url == temp_database_url

    async def test_add_and_retrieve_message(self, temp_database_url):
        """Test adding and retrieving a message."""
        memory = LongTermMemory(temp_database_url)

        await memory.add_message("user", "Test message", session_id="test")
        messages = await memory.get_messages(session_id="test")

        assert len(messages) == 1
        assert messages[0].role == "user"
        assert messages[0].content == "Test message"
        assert messages[0].session_id == "test"

    async def test_persistence(self, temp_database_url):
        """Test that messages persist across instances."""
        # First instance
        memory1 = LongTermMemory(temp_database_url)
        await memory1.add_message("user", "Persistent message", session_id="test")

        # Second instance with same database
        memory2 = LongTermMemory(temp_database_url)
        messages = await memory2.get_messages(session_id="test")

        assert len(messages) == 1
        assert messages[0].content == "Persistent message"

    async def test_multiple_sessions(self, temp_database_url):
        """Test handling multiple sessions."""
        memory = LongTermMemory(temp_database_url)

        await memory.add_message("user", "Session 1 msg", session_id="session1")
        await memory.add_message("user", "Session 2 msg", session_id="session2")
        await memory.add_message("user", "Another session 1", session_id="session1")

        session1_msgs = await memory.get_messages(session_id="session1")
        assert len(session1_msgs) == 2

        session2_msgs = await memory.get_messages(session_id="session2")
        assert len(session2_msgs) == 1

    async def test_get_messages_with_limit(self, temp_database_url):
        """Test retrieving messages with limit."""
        memory = LongTermMemory(temp_database_url)

        # Add 10 messages
        for i in range(10):
            await memory.add_message("user", f"Message {i}", session_id="test")

        messages = await memory.get_messages(session_id="test", limit=5)
        assert len(messages) == 5
        # Should get last 5 messages
        assert messages[0].content == "Message 5"
        assert messages[-1].content == "Message 9"

    async def test_clear_session(self, temp_database_url):
        """Test clearing a specific session."""
        memory = LongTermMemory(temp_database_url)

        await memory.add_message("user", "Session 1", session_id="session1")
        await memory.add_message("user", "Session 2", session_id="session2")

        await memory.clear(session_id="session1")

        session1_msgs = await memory.get_messages(session_id="session1")
        assert len(session1_msgs) == 0

        session2_msgs = await memory.get_messages(session_id="session2")
        assert len(session2_msgs) == 1

    async def test_clear_all(self, temp_database_url):
        """Test clearing all messages."""
        memory = LongTermMemory(temp_database_url)

        await memory.add_message("user", "Test 1", session_id="session1")
        await memory.add_message("user", "Test 2", session_id="session2")

        await memory.clear()

        all_msgs = await memory.get_messages()
        assert len(all_msgs) == 0

    async def test_get_context(self, temp_database_url):
        """Test getting context for LLM."""
        memory = LongTermMemory(temp_database_url)

        await memory.add_message("system", "System prompt", session_id="test")
        await memory.add_message("user", "Hello", session_id="test")
        await memory.add_message("assistant", "Hi!", session_id="test")

        context = await memory.get_context(session_id="test")

        assert len(context) == 3
        assert all(isinstance(msg, dict) for msg in context)
        assert context[0]["role"] == "system"
        assert context[1]["role"] == "user"
        assert context[2]["role"] == "assistant"

    async def test_get_all_sessions(self, temp_database_url):
        """Test getting all session IDs."""
        memory = LongTermMemory(temp_database_url)

        await memory.add_message("user", "Msg 1", session_id="session1")
        await memory.add_message("user", "Msg 2", session_id="session2")
        await memory.add_message("user", "Msg 3", session_id="session3")

        sessions = await memory.get_all_sessions()
        assert len(sessions) == 3
        assert "session1" in sessions
        assert "session2" in sessions
        assert "session3" in sessions

    async def test_get_session_message_count(self, temp_database_url):
        """Test getting message count for a session."""
        memory = LongTermMemory(temp_database_url)

        for i in range(5):
            await memory.add_message("user", f"Msg {i}", session_id="test")

        count = await memory.get_session_message_count("test")
        assert count == 5

    async def test_message_ordering(self, temp_database_url):
        """Test that messages are ordered by timestamp."""
        memory = LongTermMemory(temp_database_url)

        await memory.add_message("user", "First", session_id="test")
        await memory.add_message("user", "Second", session_id="test")
        await memory.add_message("user", "Third", session_id="test")

        messages = await memory.get_messages(session_id="test")

        assert messages[0].content == "First"
        assert messages[1].content == "Second"
        assert messages[2].content == "Third"

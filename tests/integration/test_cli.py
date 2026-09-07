"""Integration tests for CLI functionality."""

from unittest.mock import patch

import pytest

from lotusette.ui.cli import LotusetteCLI


def _fake_stream(chunks):
    """Build a generate_stream replacement yielding the given chunks."""

    async def _stream(_messages):
        for chunk in chunks:
            yield chunk

    return _stream


@pytest.mark.asyncio
class TestLotusetteCLI:
    """Integration tests for CLI."""

    @patch("lotusette.ui.cli.settings")
    async def test_initialization_openai(self, mock_settings, temp_database_url):
        """Test CLI initialization with OpenAI."""
        mock_settings.llm_provider = "openai"
        mock_settings.openai_api_key = "test-key"
        mock_settings.openai_model = "gpt-4-turbo-preview"
        mock_settings.database_url = temp_database_url

        cli = LotusetteCLI()
        success = await cli.initialize()

        assert success is True
        assert cli.initialized is True
        assert cli.llm is not None
        assert cli.llm.provider_name == "openai"

    @patch("lotusette.ui.cli.settings")
    async def test_initialization_claude(self, mock_settings, temp_database_url):
        """Test CLI initialization with Claude."""
        mock_settings.llm_provider = "claude"
        mock_settings.anthropic_api_key = "test-key"
        mock_settings.anthropic_model = "claude-3-opus-20240229"
        mock_settings.database_url = temp_database_url

        cli = LotusetteCLI()
        success = await cli.initialize()

        assert success is True
        assert cli.initialized is True
        assert cli.llm is not None
        assert cli.llm.provider_name == "claude"

    @patch("lotusette.ui.cli.settings")
    async def test_initialization_missing_api_key(self, mock_settings, temp_database_url):
        """Test initialization fails with missing API key."""
        mock_settings.llm_provider = "openai"
        mock_settings.openai_api_key = None
        mock_settings.database_url = temp_database_url

        cli = LotusetteCLI()
        success = await cli.initialize()

        assert success is False
        assert cli.initialized is False

    @patch("lotusette.ui.cli.settings")
    async def test_chat_flow(self, mock_settings, temp_database_url):
        """Test complete chat flow."""
        mock_settings.llm_provider = "openai"
        mock_settings.openai_api_key = "test-key"
        mock_settings.openai_model = "gpt-4"
        mock_settings.database_url = temp_database_url
        mock_settings.llm_context_messages = 20

        cli = LotusetteCLI()
        await cli.initialize()

        # Le CLI consomme generate_stream, pas generate.
        cli.llm.generate_stream = _fake_stream(["Hello! ", "How can I ", "help you?"])

        # Simulate user input
        await cli.chat("Hello")

        # Verify message was added to memory
        messages = await cli.short_term_memory.get_messages(cli.session_id)
        assert len(messages) >= 2  # At least user message and assistant response

        # Find user and assistant messages
        user_msgs = [m for m in messages if m.role == "user"]
        assistant_msgs = [m for m in messages if m.role == "assistant"]

        assert len(user_msgs) >= 1
        assert len(assistant_msgs) >= 1
        assert user_msgs[-1].content == "Hello"
        assert assistant_msgs[-1].content == "Hello! How can I help you?"

    @patch("lotusette.ui.cli.settings")
    async def test_initialization_local(self, mock_settings, temp_database_url):
        """Le provider local démarre sans aucune clé d'API."""
        mock_settings.llm_provider = "local"
        mock_settings.local_llm_model = "Ministral-3-14B-Instruct"
        mock_settings.local_llm_base_url = "http://localhost:8080/v1"
        mock_settings.local_llm_api_key = "EMPTY"
        mock_settings.llm_temperature = 0.7
        mock_settings.llm_max_tokens = 1000
        mock_settings.database_url = temp_database_url

        cli = LotusetteCLI()
        success = await cli.initialize()

        assert success is True
        assert cli.llm.provider_name == "local"
        assert cli.llm.model == "Ministral-3-14B-Instruct"
        assert cli.llm.base_url == "http://localhost:8080/v1"

    @patch("lotusette.ui.cli.settings")
    async def test_initialization_local_vllm_alias(self, mock_settings, temp_database_url):
        """L'ancien nom local-vllm reste accepté."""
        mock_settings.llm_provider = "local-vllm"
        mock_settings.local_llm_model = "test-model"
        mock_settings.local_llm_base_url = "http://localhost:8080/v1"
        mock_settings.local_llm_api_key = "EMPTY"
        mock_settings.llm_temperature = 0.7
        mock_settings.llm_max_tokens = 1000
        mock_settings.database_url = temp_database_url

        cli = LotusetteCLI()

        assert await cli.initialize() is True
        assert cli.llm.provider_name == "local"

    @patch("lotusette.ui.cli.settings")
    async def test_initialization_unknown_provider(self, mock_settings, temp_database_url):
        """Un provider inconnu interrompt le démarrage sans lever."""
        mock_settings.llm_provider = "gpt5-turbo-max"
        mock_settings.database_url = temp_database_url

        cli = LotusetteCLI()

        assert await cli.initialize() is False
        assert cli.initialized is False

    @patch("lotusette.ui.cli.settings")
    async def test_chat_measures_time_to_first_token(self, mock_settings, temp_database_url):
        """Le flux renvoie une latence de premier token et un débit."""
        mock_settings.llm_provider = "openai"
        mock_settings.openai_api_key = "test-key"
        mock_settings.openai_model = "gpt-4"
        mock_settings.database_url = temp_database_url
        mock_settings.llm_context_messages = 20

        cli = LotusetteCLI()
        await cli.initialize()
        cli.llm.generate_stream = _fake_stream(["a", "b", "c"])

        content, ttft, elapsed, chunks, interrupted = await cli._stream_reply([])

        assert content == "abc"
        assert ttft is not None and ttft >= 0
        assert elapsed >= 0
        assert chunks == 3
        assert interrupted is False

    @patch("lotusette.ui.cli.settings")
    async def test_chat_with_empty_stream(self, mock_settings, temp_database_url):
        """Un flux vide ne doit rien écrire en mémoire."""
        mock_settings.llm_provider = "openai"
        mock_settings.openai_api_key = "test-key"
        mock_settings.openai_model = "gpt-4"
        mock_settings.database_url = temp_database_url
        mock_settings.llm_context_messages = 20

        cli = LotusetteCLI()
        await cli.initialize()
        cli.llm.generate_stream = _fake_stream([])

        await cli.chat("Hello")

        messages = await cli.short_term_memory.get_messages(cli.session_id)
        assert [m.role for m in messages if m.role == "assistant"] == []

    @patch("lotusette.ui.cli.settings")
    async def test_chat_reply_with_rich_markup(self, mock_settings, temp_database_url):
        """Une réponse contenant des crochets est stockée telle quelle."""
        mock_settings.llm_provider = "openai"
        mock_settings.openai_api_key = "test-key"
        mock_settings.openai_model = "gpt-4"
        mock_settings.database_url = temp_database_url
        mock_settings.llm_context_messages = 20

        cli = LotusetteCLI()
        await cli.initialize()
        cli.llm.generate_stream = _fake_stream(["Utilise ", "list[int] ", "[/red]"])

        await cli.chat("Hello")

        assistant = [
            m
            for m in await cli.short_term_memory.get_messages(cli.session_id)
            if m.role == "assistant"
        ]
        assert assistant[-1].content == "Utilise list[int] [/red]"

    async def test_command_clear(self):
        """Test /clear command."""
        cli = LotusetteCLI()

        # Add some messages
        await cli.short_term_memory.add_message("user", "Test", cli.session_id)
        await cli.short_term_memory.add_message("assistant", "Response", cli.session_id)

        # Clear should continue execution
        should_continue = await cli.handle_command("/clear")
        assert should_continue is True

        # Only system message should remain
        messages = await cli.short_term_memory.get_messages(cli.session_id)
        system_msgs = [m for m in messages if m.role == "system"]
        user_msgs = [m for m in messages if m.role != "system"]

        assert len(system_msgs) == 1
        assert len(user_msgs) == 0

    async def test_command_exit(self):
        """Test /exit command."""
        cli = LotusetteCLI()
        should_continue = await cli.handle_command("/exit")
        assert should_continue is False

        should_continue = await cli.handle_command("/quit")
        assert should_continue is False

    async def test_command_stats(self):
        """Test /stats command."""
        cli = LotusetteCLI()

        await cli.short_term_memory.add_message("user", "Test 1", cli.session_id)
        await cli.short_term_memory.add_message("user", "Test 2", cli.session_id)

        should_continue = await cli.handle_command("/stats")
        assert should_continue is True

    async def test_memory_persistence(self, temp_database_url):
        """Test that messages persist in long-term memory."""
        from lotusette.core.memory import LongTermMemory

        cli = LotusetteCLI()
        cli.long_term_memory = LongTermMemory(temp_database_url)

        # Add messages
        await cli.short_term_memory.add_message("user", "Test message", cli.session_id)
        await cli.long_term_memory.add_message("user", "Test message", cli.session_id)

        # Retrieve from long-term memory
        messages = await cli.long_term_memory.get_messages(cli.session_id)
        assert len(messages) == 1
        assert messages[0].content == "Test message"

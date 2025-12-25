"""Integration tests for CLI functionality."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from io import StringIO

from lotusette.ui.cli import LotusetteCLI
from lotusette.core.llm import Message, LLMResponse


@pytest.mark.asyncio
class TestLotusetteCLI:
    """Integration tests for CLI."""
    
    @patch('lotusette.ui.cli.settings')
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
    
    @patch('lotusette.ui.cli.settings')
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
    
    @patch('lotusette.ui.cli.settings')
    async def test_initialization_missing_api_key(self, mock_settings, temp_database_url):
        """Test initialization fails with missing API key."""
        mock_settings.llm_provider = "openai"
        mock_settings.openai_api_key = None
        mock_settings.database_url = temp_database_url
        
        cli = LotusetteCLI()
        success = await cli.initialize()
        
        assert success is False
        assert cli.initialized is False
    
    @patch('lotusette.ui.cli.settings')
    async def test_chat_flow(self, mock_settings, temp_database_url):
        """Test complete chat flow."""
        mock_settings.llm_provider = "openai"
        mock_settings.openai_api_key = "test-key"
        mock_settings.openai_model = "gpt-4"
        mock_settings.database_url = temp_database_url
        
        cli = LotusetteCLI()
        await cli.initialize()
        
        # Mock LLM response
        mock_response = LLMResponse(
            content="Hello! How can I help you?",
            model="gpt-4",
            tokens_used=25,
            finish_reason="stop"
        )
        cli.llm.generate = AsyncMock(return_value=mock_response)
        
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

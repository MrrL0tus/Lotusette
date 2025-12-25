"""Unit tests for prompt manager."""

import pytest
from lotusette.core.llm import PromptManager


class TestPromptManager:
    """Tests for PromptManager."""
    
    def test_default_prompt(self):
        """Test that default prompt is set."""
        manager = PromptManager()
        prompt = manager.get_system_prompt()
        assert isinstance(prompt, str)
        assert len(prompt) > 0
        assert "Lotusette" in prompt
    
    def test_custom_prompt(self):
        """Test setting a custom prompt."""
        custom = "Custom system prompt"
        manager = PromptManager(custom_system_prompt=custom)
        assert manager.get_system_prompt() == custom
    
    def test_set_system_prompt(self):
        """Test setting prompt after initialization."""
        manager = PromptManager()
        new_prompt = "New system prompt"
        manager.set_system_prompt(new_prompt)
        assert manager.get_system_prompt() == new_prompt
    
    def test_reset_to_default(self):
        """Test resetting to default prompt."""
        manager = PromptManager()
        original = manager.get_system_prompt()
        
        manager.set_system_prompt("Temporary prompt")
        assert manager.get_system_prompt() != original
        
        manager.reset_to_default()
        assert manager.get_system_prompt() == original
    
    def test_format_with_context(self):
        """Test formatting prompt with additional context."""
        manager = PromptManager()
        original = manager.get_system_prompt()
        context = "Additional context information"
        
        formatted = manager.format_with_context(context)
        assert original in formatted
        assert context in formatted
        assert formatted == f"{original}\n\n{context}"

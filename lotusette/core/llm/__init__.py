"""LLM module initialization."""

from .base import BaseLLM, LLMResponse, Message
from .claude_provider import ClaudeProvider
from .factory import LLMFactory
from .local_openai_provider import LocalOpenAIProvider, LocalVLLMProvider
from .openai_provider import OpenAIProvider
from .prompt_manager import PromptManager

__all__ = [
    "BaseLLM",
    "Message",
    "LLMResponse",
    "OpenAIProvider",
    "ClaudeProvider",
    "LocalOpenAIProvider",
    # Ancien nom du provider local, conservé pour compatibilité.
    "LocalVLLMProvider",
    "PromptManager",
    "LLMFactory",
]

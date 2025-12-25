"""Base LLM interface for Lotusette."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import AsyncIterator, Dict, List, Optional


@dataclass
class Message:
    """Represents a conversation message."""

    role: str  # 'system', 'user', 'assistant'
    content: str

    def to_dict(self) -> Dict[str, str]:
        """Convert message to dictionary format."""
        return {"role": self.role, "content": self.content}


@dataclass
class LLMResponse:
    """Represents a response from the LLM."""

    content: str
    model: str
    tokens_used: Optional[int] = None
    finish_reason: Optional[str] = None


class BaseLLM(ABC):
    """Abstract base class for LLM providers."""

    def __init__(self, model: str, temperature: float = 0.7, max_tokens: int = 1000):
        """Initialize the LLM provider.

        Args:
            model: The model identifier to use
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
        """
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    @abstractmethod
    async def generate(self, messages: List[Message], stream: bool = False) -> LLMResponse:
        """Generate a response from the LLM.

        Args:
            messages: List of conversation messages
            stream: Whether to stream the response

        Returns:
            LLMResponse containing the generated text
        """
        pass

    @abstractmethod
    async def generate_stream(self, messages: List[Message]) -> AsyncIterator[str]:
        """Generate a streaming response from the LLM.

        Args:
            messages: List of conversation messages

        Yields:
            Chunks of generated text
        """
        pass

    def create_message(self, role: str, content: str) -> Message:
        """Helper method to create a message.

        Args:
            role: Message role (system, user, assistant)
            content: Message content

        Returns:
            Message instance
        """
        return Message(role=role, content=content)

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the name of the LLM provider."""
        pass

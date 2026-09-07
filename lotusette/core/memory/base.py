"""Base memory interface for Lotusette."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ConversationMessage:
    """Represents a message in the conversation history."""

    role: str
    content: str
    timestamp: datetime
    session_id: str | None = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "session_id": self.session_id,
        }


class BaseMemory(ABC):
    """Abstract base class for memory systems."""

    @abstractmethod
    async def add_message(self, role: str, content: str, session_id: str | None = None) -> None:
        """Add a message to memory.

        Args:
            role: Message role (user, assistant, system)
            content: Message content
            session_id: Optional session identifier
        """
        pass

    @abstractmethod
    async def get_messages(
        self, session_id: str | None = None, limit: int | None = None
    ) -> list[ConversationMessage]:
        """Retrieve messages from memory.

        Args:
            session_id: Optional session to filter by
            limit: Optional limit on number of messages

        Returns:
            List of conversation messages
        """
        pass

    @abstractmethod
    async def clear(self, session_id: str | None = None) -> None:
        """Clear messages from memory.

        Args:
            session_id: Optional session to clear (None = clear all)
        """
        pass

    @abstractmethod
    async def get_context(
        self, session_id: str | None = None, max_messages: int = 10
    ) -> list[dict[str, str]]:
        """Get conversation context for LLM.

        Args:
            session_id: Optional session identifier
            max_messages: Maximum number of messages to include

        Returns:
            List of message dicts in LLM format
        """
        pass

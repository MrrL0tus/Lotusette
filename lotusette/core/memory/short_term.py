"""Short-term memory implementation using in-memory storage."""

import logging
from typing import List, Dict, Optional
from datetime import datetime
from collections import deque

from .base import BaseMemory, ConversationMessage

logger = logging.getLogger(__name__)


class ShortTermMemory(BaseMemory):
    """In-memory storage for short-term conversation context."""
    
    def __init__(self, max_messages: int = 100):
        """Initialize short-term memory.
        
        Args:
            max_messages: Maximum number of messages to keep in memory
        """
        self.max_messages = max_messages
        self._messages: deque = deque(maxlen=max_messages)
        logger.info(f"Initialized short-term memory with capacity: {max_messages}")
    
    async def add_message(
        self,
        role: str,
        content: str,
        session_id: Optional[str] = None
    ) -> None:
        """Add a message to short-term memory.
        
        Args:
            role: Message role (user, assistant, system)
            content: Message content
            session_id: Optional session identifier
        """
        message = ConversationMessage(
            role=role,
            content=content,
            timestamp=datetime.now(),
            session_id=session_id
        )
        self._messages.append(message)
        logger.debug(f"Added {role} message to short-term memory (total: {len(self._messages)})")
    
    async def get_messages(
        self,
        session_id: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[ConversationMessage]:
        """Retrieve messages from short-term memory.
        
        Args:
            session_id: Optional session to filter by
            limit: Optional limit on number of messages
            
        Returns:
            List of conversation messages
        """
        messages = list(self._messages)
        
        # Filter by session if specified
        if session_id is not None:
            messages = [m for m in messages if m.session_id == session_id]
        
        # Apply limit if specified
        if limit is not None:
            messages = messages[-limit:]
        
        return messages
    
    async def clear(self, session_id: Optional[str] = None) -> None:
        """Clear messages from short-term memory.
        
        Args:
            session_id: Optional session to clear (None = clear all)
        """
        if session_id is None:
            self._messages.clear()
            logger.info("Cleared all messages from short-term memory")
        else:
            # Remove only messages from specific session
            self._messages = deque(
                [m for m in self._messages if m.session_id != session_id],
                maxlen=self.max_messages
            )
            logger.info(f"Cleared messages for session {session_id} from short-term memory")
    
    async def get_context(
        self,
        session_id: Optional[str] = None,
        max_messages: int = 10
    ) -> List[Dict[str, str]]:
        """Get conversation context for LLM.
        
        Args:
            session_id: Optional session identifier
            max_messages: Maximum number of messages to include
            
        Returns:
            List of message dicts in LLM format
        """
        messages = await self.get_messages(session_id=session_id, limit=max_messages)
        return [{"role": m.role, "content": m.content} for m in messages]
    
    def get_message_count(self, session_id: Optional[str] = None) -> int:
        """Get the count of messages in memory.
        
        Args:
            session_id: Optional session to filter by
            
        Returns:
            Number of messages
        """
        if session_id is None:
            return len(self._messages)
        return sum(1 for m in self._messages if m.session_id == session_id)

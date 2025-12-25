"""Long-term memory implementation using database storage."""

import logging
from datetime import datetime
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from .base import BaseMemory, ConversationMessage
from .models import ConversationModel, init_db

logger = logging.getLogger(__name__)


class LongTermMemory(BaseMemory):
    """Persistent storage for long-term conversation history."""

    def __init__(self, database_url: str):
        """Initialize long-term memory with database.

        Args:
            database_url: SQLAlchemy database URL
        """
        self.database_url = database_url
        self.engine, self.SessionLocal = init_db(database_url)
        logger.info(f"Initialized long-term memory with database: {database_url}")

    def _get_session(self) -> Session:
        """Get a database session."""
        return self.SessionLocal()

    async def add_message(self, role: str, content: str, session_id: Optional[str] = None) -> None:
        """Add a message to long-term storage.

        Args:
            role: Message role (user, assistant, system)
            content: Message content
            session_id: Optional session identifier
        """
        db = self._get_session()
        try:
            conversation = ConversationModel(
                session_id=session_id or "default",
                role=role,
                content=content,
                timestamp=datetime.now(),
            )
            db.add(conversation)
            db.commit()
            logger.debug(f"Added {role} message to long-term storage")
        except Exception as e:
            db.rollback()
            logger.error(f"Error adding message to long-term storage: {e}")
            raise
        finally:
            db.close()

    async def get_messages(
        self, session_id: Optional[str] = None, limit: Optional[int] = None
    ) -> List[ConversationMessage]:
        """Retrieve messages from long-term storage.

        Args:
            session_id: Optional session to filter by
            limit: Optional limit on number of messages

        Returns:
            List of conversation messages
        """
        db = self._get_session()
        try:
            query = db.query(ConversationModel)

            if session_id is not None:
                query = query.filter(ConversationModel.session_id == session_id)

            query = query.order_by(ConversationModel.timestamp.asc())

            if limit is not None:
                # Get the last N messages
                total = query.count()
                if total > limit:
                    query = query.offset(total - limit)

            results = query.all()

            messages = [
                ConversationMessage(
                    role=r.role, content=r.content, timestamp=r.timestamp, session_id=r.session_id
                )
                for r in results
            ]

            return messages

        finally:
            db.close()

    async def clear(self, session_id: Optional[str] = None) -> None:
        """Clear messages from long-term storage.

        Args:
            session_id: Optional session to clear (None = clear all)
        """
        db = self._get_session()
        try:
            query = db.query(ConversationModel)

            if session_id is not None:
                query = query.filter(ConversationModel.session_id == session_id)
                count = query.delete()
                logger.info(f"Cleared {count} messages for session {session_id}")
            else:
                count = query.delete()
                logger.info(f"Cleared all {count} messages from long-term storage")

            db.commit()

        except Exception as e:
            db.rollback()
            logger.error(f"Error clearing long-term storage: {e}")
            raise
        finally:
            db.close()

    async def get_context(
        self, session_id: Optional[str] = None, max_messages: int = 10
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

    async def get_all_sessions(self) -> List[str]:
        """Get list of all session IDs.

        Returns:
            List of unique session IDs
        """
        db = self._get_session()
        try:
            sessions = db.query(ConversationModel.session_id).distinct().all()
            return [s[0] for s in sessions]
        finally:
            db.close()

    async def get_session_message_count(self, session_id: str) -> int:
        """Get count of messages in a session.

        Args:
            session_id: Session identifier

        Returns:
            Number of messages in the session
        """
        db = self._get_session()
        try:
            count = (
                db.query(ConversationModel)
                .filter(ConversationModel.session_id == session_id)
                .count()
            )
            return count
        finally:
            db.close()

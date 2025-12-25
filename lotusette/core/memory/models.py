"""Database models for conversation storage."""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class ConversationModel(Base):
    """Database model for storing conversation messages."""

    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(255), nullable=False, index=True)
    role = Column(String(50), nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(), nullable=False)

    def __repr__(self):
        return f"<Conversation(id={self.id}, session={self.session_id}, role={self.role})>"

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": self.id,
            "session_id": self.session_id,
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
        }


def init_db(database_url: str):
    """Initialize the database.

    Args:
        database_url: SQLAlchemy database URL

    Returns:
        Tuple of (engine, SessionLocal)
    """
    engine = create_engine(database_url, echo=False)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, SessionLocal

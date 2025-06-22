from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, String, DateTime, Text, Boolean, ForeignKey
from datetime import datetime, timezone

from config import settings

# Database engine for asynchronous operations
# Use asyncpg driver for PostgreSQL
# Ensure DATABASE_URL uses 'asyncpg' as the driver, e.g., 'postgresql+asyncpg://user:pass@host/db'
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Asynchronous session maker
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False # Prevents objects from expiring after commit
)

Base = declarative_base()

# --- SQLAlchemy ORM Models ---
# These models define the database tables.

class User(Base):
    """SQLAlchemy model for the 'users' table."""
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True) # Using String for UUIDs
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    created_at = Column(DateTime, default=datetime.utcnow)

class Message(Base):
    """SQLAlchemy model for the 'messages' table."""
    __tablename__ = "messages"
    id = Column(String, primary_key=True, index=True)
    sender_id = Column(String, ForeignKey("users.id"))
    receiver_id = Column(String, ForeignKey("users.id"), nullable=True) # For direct messages
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    timestamp = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)
    # Consider adding a 'chat_room_id' if general chat rooms are needed

class Questionnaire(Base):
    """SQLAlchemy model for the 'questionnaires' table."""
    __tablename__ = "questionnaires"
    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    questions_json = Column(Text) # Store questions as JSON string
    created_at = Column(DateTime, default=datetime.utcnow)

class QuestionnaireSession(Base):
    """SQLAlchemy model for the 'questionnaire_sessions' table."""
    __tablename__ = "questionnaire_sessions"
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    status = Column(String, default="started") # e.g., "started", "completed", "aborted"

class Answer(Base):
    """SQLAlchemy model for the 'answers' table."""
    __tablename__ = "answers"
    id = Column(String, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("questionnaire_sessions.id"))
    question_id = Column(String) # ID of the question within the questionnaire
    answer_text = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

class ClinicalInsight(Base):
    """SQLAlchemy model for the 'clinical_insights' table."""
    __tablename__ = "clinical_insights"
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    source_type = Column(String) # e.g., "message_analysis", "questionnaire_summary"
    source_id = Column(String, nullable=True) # ID of the message/session that triggered insight
    insight_text = Column(Text)
    severity = Column(String, nullable=True) # e.g., "low", "medium", "high"
    recommendations = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


async def get_db():
    """
    Dependency to get an asynchronous database session.
    Yields a session and ensures it's closed after use.
    """
    async with AsyncSessionLocal() as session:
        yield session

async def create_db_and_tables():
    """
    Creates all defined database tables.
    Should be called on application startup.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created or already exist.")

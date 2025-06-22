import uuid
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from datetime import datetime

from database import Message as DBMessage
from models.message import MessageCreate, Message # Pydantic models

class MessageRepository:
    """
    Repository class for Message data operations.
    Handles interaction with the database for Message entities.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_message(self, message_data: MessageCreate) -> DBMessage:
        """Creates a new message in the database."""
        message_id = str(uuid.uuid4())
        new_message = DBMessage(
            id=message_id,
            sender_id=message_data.sender_id,
            receiver_id=message_data.receiver_id,
            content=message_data.content,
            is_read=message_data.is_read,
            timestamp=datetime.utcnow()
        )
        self.db.add(new_message)
        await self.db.commit()
        await self.db.refresh(new_message)
        return new_message

    async def get_message_by_id(self, message_id: str) -> Optional[DBMessage]:
        """Fetches a message by its ID."""
        stmt = select(DBMessage).where(DBMessage.id == message_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_messages_for_user(self, user_id: str) -> List[DBMessage]:
        """Fetches all messages where the user is either sender or receiver."""
        stmt = select(DBMessage).where(
            (DBMessage.sender_id == user_id) | (DBMessage.receiver_id == user_id)
        ).order_by(DBMessage.timestamp)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_conversation(self, user1_id: str, user2_id: str) -> List[DBMessage]:
        """Fetches messages between two specific users (direct messages)."""
        stmt = select(DBMessage).where(
            ((DBMessage.sender_id == user1_id) & (DBMessage.receiver_id == user2_id)) |
            ((DBMessage.sender_id == user2_id) & (DBMessage.receiver_id == user1_id))
        ).order_by(DBMessage.timestamp)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def mark_message_as_read(self, message_id: str) -> Optional[DBMessage]:
        """Marks a specific message as read."""
        stmt = update(DBMessage).where(DBMessage.id == message_id).values(is_read=True).returning(DBMessage)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalars().first()

    async def delete_message(self, message_id: str) -> bool:
        """Deletes a message by its ID."""
        stmt = delete(DBMessage).where(DBMessage.id == message_id)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.rowcount > 0



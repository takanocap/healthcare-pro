from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class MessageBase(BaseModel):
    """Base Pydantic model for Message data."""
    content: str = Field(min_length=1)
    is_read: bool = False

class MessageCreate(MessageBase):
    """Pydantic model for creating a new Message."""
    sender_id: str
    receiver_id: Optional[str] = None # Optional for direct messages

class Message(MessageBase):
    """Pydantic model for Message data retrieved from the database."""
    id: str
    sender_id: str
    receiver_id: Optional[str] = None
    timestamp: datetime

    class Config:
        """Pydantic configuration for ORM mode."""
        from_attributes = True
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Pydantic models for request/response bodies and validation

class UserBase(BaseModel):
    """Base Pydantic model for User data."""
    username: str = Field(min_length=3, max_length=50)
    email: str = Field(pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

class UserCreate(UserBase):
    """Pydantic model for creating a new User, including password."""
    password: str = Field(min_length=8)

class User(UserBase):
    """Pydantic model for User data retrieved from the database."""
    id: str
    created_at: datetime

    class Config:
        """Pydantic configuration for ORM mode."""
        from_attributes = True # Allow mapping from SQLAlchemy ORM models
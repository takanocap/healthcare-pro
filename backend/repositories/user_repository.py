import uuid
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import selectinload

from database import User as DBUser
from models.user import UserCreate, User # Assuming Pydantic User for return type

class UserRepository:
    """
    Repository class for User data operations.
    Handles interaction with the database for User entities.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user_data: UserCreate) -> DBUser:
        """
        Creates a new user in the database.
        Note: Hashing password should happen in service layer.
        """
        user_id = str(uuid.uuid4())
        new_user = DBUser(
            id=user_id,
            username=user_data.username,
            email=user_data.email,
            hashed_password=user_data.password # Hashed in service, just passed here
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user

    async def get_user_by_id(self, user_id: str) -> Optional[DBUser]:
        """Fetches a user by their ID."""
        stmt = select(DBUser).where(DBUser.id == user_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_user_by_username(self, username: str) -> Optional[DBUser]:
        """Fetches a user by their username."""
        stmt = select(DBUser).where(DBUser.username == username)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_user_by_email(self, email: str) -> Optional[DBUser]:
        """Fetches a user by their email address."""
        stmt = select(DBUser).where(DBUser.email == email)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_all_users(self) -> List[DBUser]:
        """Fetches all users from the database."""
        stmt = select(DBUser)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update_user(self, user_id: str, updates: dict) -> Optional[DBUser]:
        """
        Updates an existing user's information.
        'updates' should be a dictionary of fields to update.
        """
        stmt = update(DBUser).where(DBUser.id == user_id).values(**updates).returning(DBUser)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalars().first()

    async def delete_user(self, user_id: str) -> bool:
        """Deletes a user by their ID."""
        stmt = delete(DBUser).where(DBUser.id == user_id)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.rowcount > 0 # Returns True if a row was deleted
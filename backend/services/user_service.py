from typing import Optional
from passlib.context import CryptContext # For password hashing
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.user_repository import UserRepository
from models.user import UserCreate, User # Pydantic models for service input/output

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    """
    Service layer for User-related business logic.
    Handles user registration, authentication, and data retrieval.
    """
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def hash_password(self, password: str) -> str:
        """Hashes a plain-text password."""
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifies a plain-text password against a hashed password."""
        return pwd_context.verify(plain_password, hashed_password)

    async def register_user(self, user_data: UserCreate) -> Optional[User]:
        """
        Registers a new user.
        Checks for existing username/email and hashes the password.
        """
        # Check if username or email already exists
        if await self.user_repo.get_user_by_username(user_data.username):
            print(f"Username '{user_data.username}' already taken.")
            return None
        if await self.user_repo.get_user_by_email(user_data.email):
            print(f"Email '{user_data.email}' already registered.")
            return None

        # Hash the password before storing
        hashed_password = self.hash_password(user_data.password)
        user_data.password = hashed_password # Update Pydantic model with hashed password

        db_user = await self.user_repo.create_user(user_data)
        return User.model_validate(db_user) # Convert SQLAlchemy model to Pydantic model

    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Authenticates a user by username and password.
        """
        db_user = await self.user_repo.get_user_by_username(username)
        if not db_user or not self.verify_password(password, db_user.hashed_password):
            return None
        return User.model_validate(db_user)

    async def get_user(self, user_id: str) -> Optional[User]:
        """Retrieves a user by ID."""
        db_user = await self.user_repo.get_user_by_id(user_id)
        if db_user:
            return User.model_validate(db_user)
        return None
from sqlalchemy import Column, Integer, String, Date

from app.database import Base


class User(Base):
    """User Model"""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    date_of_birth = Column(Date)

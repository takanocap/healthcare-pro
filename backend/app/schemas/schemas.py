from datetime import date
from typing import Optional
from pydantic import BaseModel


class UserLogin(BaseModel):
    """Schema of user login request"""
    username: str
    date_of_birth: date


class UserResponse(BaseModel):
    """Schema of user login response"""
    id: int
    username: str
    date_of_birth: date
    condition: str
    language: str

    class Config:
        orm_mode = True

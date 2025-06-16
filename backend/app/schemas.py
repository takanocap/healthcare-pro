from pydantic import BaseModel
from datetime import date

class UserLogin(BaseModel):
    username: str
    date_of_birth: date

class UserResponse(BaseModel):
    id: int
    username: str
    date_of_birth: date

    class Config:
        orm_mode = True
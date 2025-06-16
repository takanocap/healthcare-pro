from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import sys
import os
sys.path.append(os.path.dirname(__file__))

from database import SessionLocal, engine
from models import Base, User
from schemas import UserLogin, UserResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/login", response_model=UserResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter_by(
        username=user.username,
        date_of_birth=user.date_of_birth
    ).first()

    if existing_user:
        return existing_user

    new_user = User(username=user.username, date_of_birth=user.date_of_birth)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
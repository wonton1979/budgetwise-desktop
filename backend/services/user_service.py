from backend.database import SessionLocal
from backend.models.user import User
from datetime import datetime,UTC
from backend.schemas.user import UserCreate
from backend.utils.security import hash_password
from fastapi import HTTPException

def add_user(user:UserCreate):
    db = SessionLocal()
    existing_username = db.query(User).filter(User.username == user.username).first()
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_username:
        raise HTTPException(status_code=400,detail="Username already exists")
    if existing_email:
        raise HTTPException(status_code=400,detail="Email already exists")
    try:
        db_user = User(
            username=user.username,
            password_hash=hash_password(user.password),
            email=user.email,
            created_at=datetime.now(UTC),
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    finally:
        db.close()
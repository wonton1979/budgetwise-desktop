from backend.database import SessionLocal
from backend.models.user import User
from datetime import datetime,UTC
from backend.schemas.user import UserCreate, UserLogin
from backend.utils.security import hash_password,verify_password,create_access_token,verify_token
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

def login_user_service(user:UserLogin):
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.email == user.email).first()
        if not db_user:
            raise HTTPException(status_code=401,detail="Incorrect email or password")
        if not verify_password(user.password, db_user.password_hash):
            raise HTTPException(status_code=401,detail="Incorrect email or password")
        token = create_access_token({"sub": user.email})
        return {
            "access_token":token,
            "token_type":"bearer"
        }
    finally:
        db.close()

def fetch_current_user(token:str):
    db = SessionLocal()
    try:
        email = verify_token(token)
        db_user = db.query(User).filter(User.email == email).first()
        if not db_user:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return db_user
    finally:
        db.close()

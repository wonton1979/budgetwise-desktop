import os
from pwdlib import PasswordHash
from datetime import datetime,timezone,timedelta
import jwt

password_hash = PasswordHash.recommended()


JWT_SECRET_KEY = os.getenv('BACKEND_JWT_SECRET_KEY')
JWT_ALGORITHM = os.getenv('BACKEND_JWT_ALGORITHM')
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('BACKEND_JWT_ACCESS_TOKEN_EXPIRE_MINUTES')

if not JWT_SECRET_KEY:
    raise ValueError('SECRET_KEY must be set')


def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=int(JWT_ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


# app/core/security.py

from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
import os
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def hash_password(password: str) -> str:
    """
    Hash password safely for bcrypt.
    Bcrypt only supports up to 72 bytes, so truncate longer passwords.
    """
    if not isinstance(password, str):
        raise TypeError("Password must be a string.")
    return pwd_context.hash(password[:72])

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify plaintext password against its hash, safely handling length limits.
    """
    if not isinstance(plain_password, str):
        raise TypeError("Password must be a string.")
    try:
        return pwd_context.verify(plain_password[:72], hashed_password)
    except Exception:
        return False

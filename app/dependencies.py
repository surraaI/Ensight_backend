from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from jose import JWTError, jwt
from app.core.config import settings  # adjust based on your actual config path


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Dummy current user dependency (for now, for testing)
def get_current_user():
    raise HTTPException(status_code=401, detail="Not implemented")

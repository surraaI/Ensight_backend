# app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.services.auth_service import signup_user, login_user
from app.schemas.user import PasswordReset
from app.services.auth_service import reset_password
from app.core.security import verify_password, hash_password
from app.dependencies import get_current_user  # ADD THIS IMPORT
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=UserOut)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    return signup_user(user, db)


@router.post("/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    return login_user(credentials, db)


@router.post("/reset-password")
def password_reset(
    reset_data: PasswordReset,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return reset_password(db, current_user, reset_data.current_password, reset_data.new_password)
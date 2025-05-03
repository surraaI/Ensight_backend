from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, Token
from passlib.context import CryptContext
from jose import jwt
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET", "your-secret")
ALGORITHM = "HS256"

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup", response_model=Token)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = pwd_context.hash(user_data.password)
    new_user = User(
        id=uuid.uuid4(),
        email=user_data.email,
        hashed_password=hashed,
        role=user_data.role,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = jwt.encode({"sub": new_user.email}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not pwd_context.verify(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode({"sub": user.email}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

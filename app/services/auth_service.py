from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from app.models.user import User, Role
from app.schemas.user import UserCreate, UserLogin
from app.core.security import hash_password, verify_password
from app.core.security import create_access_token
import uuid


def signup_user(user: UserCreate, db: Session):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        id=str(uuid.uuid4()),
        email=user.email,
        hashed_password=hash_password(user.password),
        role=Role.FREE_USER,  
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(credentials: UserLogin, db: Session):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": user.id, "role": user.role},
        expires_delta=timedelta(minutes=1440)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "requires_password_reset": user.requires_password_reset 
        }
    }
    
def reset_password(db: Session, user: User, current_password: str, new_password: str):
    # Verify current password
    if not verify_password(current_password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect current password"
        )
    
    # Update password
    user.hashed_password = hash_password(new_password)
    user.requires_password_reset = False
    db.commit()
    db.refresh(user)
    return user

from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User, Role
from app.schemas.user import UserCreate
from app.core.security import hash_password
from app.utils.email_utils import send_credentials_email
from uuid import uuid4
from random import choices
import string

def generate_temp_password(length=10):
    return ''.join(choices(string.ascii_letters + string.digits, k=length))

def create_user_with_role(db: Session, user_data: UserCreate):
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already in use")

    temp_password = generate_temp_password()
    hashed_pw = hash_password(temp_password)

    new_user = User(
        id=str(uuid4()),
        email=user_data.email,
        hashed_password=hashed_pw,
        role=user_data.role,
        is_active=True,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    send_credentials_email(user_data.email, temp_password)

    return new_user

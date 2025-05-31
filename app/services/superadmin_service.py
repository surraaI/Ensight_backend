from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User, Role
from app.schemas.user import UserCreateByAdmin
from app.core.security import hash_password
from app.utils.email_utils import send_credentials_email
from uuid import uuid4
import secrets
import string

def generate_secure_temp_password(length=12):
    """Generate a cryptographically secure temporary password"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def create_user_by_admin(db: Session, user_data: UserCreateByAdmin):
    # Check if email already exists
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    
    # Validate role
    allowed_roles = [Role.ADMIN, Role.EDITOR, Role.WRITER]
    if user_data.role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role. Allowed roles: {', '.join([r.value for r in allowed_roles])}"
        )
    
    # Generate secure temporary password
    temp_password = generate_secure_temp_password()
    hashed_pw = hash_password(temp_password)
    
    # Create user
    new_user = User(
        id=str(uuid4()),
        email=user_data.email,
        hashed_password=hashed_pw,
        role=user_data.role,
        is_active=True,
        requires_password_reset=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Send credentials email (handle failure gracefully)
    email_sent = send_credentials_email(user_data.email, temp_password)
    
    if not email_sent:
        # Log this error but don't fail the request
        # Consider adding admin notification here
        print(f"Warning: Failed to send email to {user_data.email}")
    
    return new_user
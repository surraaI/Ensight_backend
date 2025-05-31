from pydantic import BaseModel, EmailStr, field_validator
from enum import Enum

class UserRole(str, Enum):
    SUPERADMIN = "SUPERADMIN"
    ADMIN = "ADMIN"
    EDITOR = "EDITOR"
    WRITER = "WRITER"
    SUBSCRIBER = "SUBSCRIBER"
    FREE_USER = "FREE_USER"

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str  # For public signup

class UserCreateByAdmin(UserBase):  # For admin-created users
    role: UserRole
    
    @field_validator('role')
    def validate_role(cls, value):
        allowed_roles = [UserRole.ADMIN, UserRole.EDITOR, UserRole.WRITER]
        if value not in allowed_roles:
            raise ValueError(f'Invalid role. Allowed: {", ".join([r.value for r in allowed_roles])}')
        return value

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PasswordReset(BaseModel):
    current_password: str
    new_password: str

class UserOut(UserBase):
    id: str
    is_active: bool
    role: UserRole
    requires_password_reset: bool  # Add this field

    class Config:
        from_attributes = True

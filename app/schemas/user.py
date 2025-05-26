from pydantic import BaseModel, EmailStr
from enum import Enum


class UserRole(str, Enum):
    superadmin = "superadmin"
    admin = "admin"
    editor = "editor"
    writer = "writer"
    subscriber = "subscriber"
    free_user = "free_user"


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str  # raw password to be hashed


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(UserBase):
    id: str
    is_active: bool
    role: UserRole

    class Config:
        from_attributes = True  # Pydantic v2 fix

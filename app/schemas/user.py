from pydantic import BaseModel, EmailStr
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    editor = "editor"
    writer = "writer"
    subscriber = "subscriber"
    free_user = "free_user"

class UserBase(BaseModel):
    email: EmailStr
    role: UserRole

class UserCreate(UserBase):
    password: str  # raw password to be hashed

class UserOut(UserBase):
    id: str
    is_active: bool

    class Config:
        orm_mode = True

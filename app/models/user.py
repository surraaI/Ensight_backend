from sqlalchemy import Column, String, Enum, Boolean
from app.database import Base
import enum
import uuid

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    WRITER = "writer"
    SUBSCRIBER = "subscriber"
    FREE_USER = "free_user"

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), default=UserRole.FREE_USER)

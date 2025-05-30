from sqlalchemy import Column, String, Enum, Boolean
from app.database import Base
import enum
import uuid

class Role(str, enum.Enum):
    SUPERADMIN = "SUPERADMIN"
    ADMIN = "ADMIN"
    EDITOR = "EDITOR"
    WRITER = "WRITER"
    SUBSCRIBER = "SUBSCRIBER"
    FREE_USER = "FREE_USER"

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(Role), default=Role.FREE_USER)
    requires_password_reset = Column(Boolean, default=False) 

    __table_args__ = {'extend_existing': True}
from sqlalchemy import Column, String, Enum, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import enum
import uuid
from datetime import datetime

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
    
    # Subscription fields
    subscription_plan_id = Column(String, ForeignKey('subscription_plans.id'), nullable=True)
    subscription_start = Column(DateTime, nullable=True)
    subscription_end = Column(DateTime, nullable=True)

    profile = relationship("Profile", uselist=False, back_populates="user")
    articles = relationship("Article", back_populates="author_user")

    __table_args__ = {'extend_existing': True}
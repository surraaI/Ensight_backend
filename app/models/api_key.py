from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from datetime import datetime
from app.database import Base
import uuid

class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    key = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    owner_id = Column(String, ForeignKey("enterprise_accounts.id"))

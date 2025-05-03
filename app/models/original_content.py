from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import uuid

class OriginalContent(Base):
    __tablename__ = "original_content"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    thumbnail_url = Column(String, nullable=True)  # <-- NEW

    status = Column(Enum("draft", "review", "published", name="content_status"), default="draft")
    is_premium = Column(Boolean, default=False)

    written_by = Column(String, ForeignKey("users.id"))
    edited_by = Column(String, ForeignKey("users.id"))
    approved_by = Column(String, ForeignKey("users.id"))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

from sqlalchemy import Column, String, Text, Boolean, Enum as SqlEnum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import uuid
from enum import Enum

class ContentStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"

class OriginalContent(Base):
    __tablename__ = "original_content"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    is_premium = Column(Boolean, default=False)
    image_url = Column(String, nullable=True)

    status = Column(SqlEnum(ContentStatus, name="original_content_status"), default=ContentStatus.DRAFT)

    written_by_id = Column(String, ForeignKey("users.id"))
    edited_by_id = Column(String, ForeignKey("users.id"))
    approved_by_id = Column(String, ForeignKey("users.id"))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=None, onupdate=datetime.utcnow)
    published_at = Column(DateTime, default=None)

from sqlalchemy import Column, String, DateTime, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM as SqlEnum
from datetime import datetime
from app.database import Base
from enum import Enum as PyEnum
from sqlalchemy import Enum as SqlEnum
import uuid

class NewsStatus(str, PyEnum):
    draft = "draft"
    published = "published"

class AggregatedNews(Base):
    __tablename__ = "aggregated_news"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    summary = Column(Text, nullable=False)
    source = Column(String, nullable=False)
    url = Column(String, nullable=False)
    thumbnail_url = Column(String, nullable=True)  # <-- NEW
    status = Column(SqlEnum(NewsStatus, name="agg_news_status"), default=NewsStatus.draft, nullable=False)
    
    written_by = Column(String, ForeignKey("users.id"))
    edited_by = Column(String, ForeignKey("users.id"))
    approved_by = Column(String, ForeignKey("users.id"))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

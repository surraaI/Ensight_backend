from sqlalchemy import (
    Column, String, Text, DateTime, Enum as SqlEnum,
    ForeignKey, Integer, Boolean
)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
from enum import Enum as PyEnum
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
    thumbnail_url = Column(String, nullable=True)

    status = Column(SqlEnum(NewsStatus, name="agg_news_status"), default=NewsStatus.draft, nullable=False)
    
    # New fields
    slug = Column(String, unique=True, index=True)
    meta_description = Column(String, nullable=True)

    is_featured = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)

    views = Column(Integer, default=0)
    shares = Column(Integer, default=0)

    category_id = Column(String, ForeignKey("categories.id"), nullable=True)
    subcategory_id = Column(String, ForeignKey("subcategories.id"), nullable=True)

    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    written_by = Column(String, ForeignKey("users.id"))
    edited_by = Column(String, ForeignKey("users.id"))
    approved_by = Column(String, ForeignKey("users.id"))

    written_by_user = relationship("User", foreign_keys=[written_by])
    edited_by_user = relationship("User", foreign_keys=[edited_by])
    approved_by_user = relationship("User", foreign_keys=[approved_by])

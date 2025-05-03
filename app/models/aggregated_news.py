from sqlalchemy import Column, String, DateTime, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import uuid

class AggregatedNewsSummary(Base):
    __tablename__ = "aggregated_news"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    summary = Column(Text, nullable=False)
    source = Column(String, nullable=False)
    url = Column(String, nullable=False)
    status = Column(Enum("draft", "published", name="agg_news_status"), default="draft")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid

class DataInsight(Base):
    __tablename__ = "data_insights"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    icon = Column(String, nullable=False)
    updated = Column(String, nullable=False)  # ISO 8601 format
    button_text = Column(String, nullable=False)
    button_link = Column(String, nullable=False)

    __table_args__ = {'extend_existing': True}
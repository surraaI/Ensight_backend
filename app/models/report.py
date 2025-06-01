from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid

class Report(Base):
    __tablename__ = "reports"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    image = Column(String, nullable=False)
    published = Column(String, nullable=False)  # ISO 8601 format
    button_text = Column(String, nullable=False)
    button_link = Column(String, nullable=False)

    __table_args__ = {'extend_existing': True}
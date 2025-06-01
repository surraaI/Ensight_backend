from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid

class Event(Base):
    __tablename__ = "events"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    date = Column(String, nullable=False)
    title = Column(String, nullable=False)
    button_text = Column(String, nullable=False)
    button_link = Column(String, nullable=False)

    __table_args__ = {'extend_existing': True}
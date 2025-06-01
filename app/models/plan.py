from sqlalchemy import Column, String, Boolean, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid

class Plan(Base):
    __tablename__ = "plans"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    price = Column(String, nullable=False)
    description = Column(String, nullable=False)
    features = Column(ARRAY(String), default=[])
    is_highlighted = Column(Boolean, default=False)

    __table_args__ = {'extend_existing': True}
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid

class Startup(Base):
    __tablename__ = "startups"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    image = Column(String, nullable=False)
    href = Column(String, nullable=False)

    __table_args__ = {'extend_existing': True}
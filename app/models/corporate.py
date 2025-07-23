from sqlalchemy import Column, String, DateTime
from app.database import Base
import uuid
from datetime import datetime
class Corporate(Base):
    __tablename__ = "corporates"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(String)
    content = Column(String)
    image = Column(String)
    profile_image = Column(String)
    name = Column(String)
    role = Column(String)
    born = Column(String)
    education = Column(String)
    mission = Column(String)
    specialties = Column(String)
    certifications = Column(String)
    motto = Column(String)
    founded = Column(String)
    quote = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

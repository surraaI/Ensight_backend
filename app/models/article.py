from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class Article(Base):
    __tablename__ = "articles"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    slug = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False, index=True)
    subcategory = Column(String, index=True)
    author = Column(String, ForeignKey("users.id"), nullable=False)
    date = Column(String, nullable=False)  # ISO 8601 format
    read_time = Column(String, nullable=False)
    image = Column(String, nullable=False)
    href = Column(String, nullable=False)
    content = Column(String, nullable=False)
    description = Column(String, nullable=False)
    is_premium = Column(Boolean, default=False)
    caption = Column(String)
    quote = Column(String)
    quote_author = Column(String)
    tag = Column(String)
    no_of_readers = Column(Integer, default=0, nullable=False)

    author_user = relationship("User", back_populates="articles")

    __table_args__ = {'extend_existing': True}
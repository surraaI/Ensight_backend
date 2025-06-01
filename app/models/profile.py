from sqlalchemy import Column, String, Boolean, ARRAY, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    avatar = Column(String)
    created_at = Column(String, nullable=False)  # ISO 8601 format
    enable_personalization = Column(Boolean, default=False)
    track_reading_progress = Column(Boolean, default=False)
    content_update_notifications = Column(Boolean, default=False)
    topics = Column(ARRAY(String), default=[])

    user = relationship("User", back_populates="profile")
    saved_articles = relationship("Article", secondary="saved_articles")
    reading_history = relationship("ReadingHistoryEntry", back_populates="profile")

    __table_args__ = {'extend_existing': True}

class ReadingHistoryEntry(Base):
    __tablename__ = "reading_history"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    profile_id = Column(String, ForeignKey("profiles.id"), nullable=False)
    article_id = Column(String, ForeignKey("articles.id"), nullable=False)
    progress = Column(Integer, nullable=False)  # 0 to 100

    profile = relationship("Profile", back_populates="reading_history")
    article = relationship("Article")

    __table_args__ = {'extend_existing': True}

# Association table for saved articles
saved_articles = Table(
    "saved_articles",
    Base.metadata,
    Column("profile_id", String, ForeignKey("profiles.id")),
    Column("article_id", String, ForeignKey("articles.id")),
    extend_existing=True
)
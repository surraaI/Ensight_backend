from sqlalchemy import Column, String, Boolean, ARRAY, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class ReadingHistoryEntry(Base):
    __tablename__ = "reading_history"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    profile_id = Column(String, ForeignKey("profiles.id"), nullable=False)
    article_id = Column(String, ForeignKey("articles.id"), nullable=False)
    progress = Column(Integer, nullable=False)  # 0 to 100

    # Explicit relationship with foreign key
    profile = relationship("Profile", back_populates="reading_history", foreign_keys=[profile_id])
    article = relationship("Article", foreign_keys=[article_id])

    __table_args__ = {'extend_existing': True}

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

    # Explicit relationship with foreign key
    user = relationship("User", back_populates="profile", foreign_keys=[user_id])
    
    # Specify primaryjoin condition
    reading_history = relationship(
        "ReadingHistoryEntry", 
        back_populates="profile",
        primaryjoin="Profile.id == ReadingHistoryEntry.profile_id"
    )

    # Explicit foreign key for saved_articles
    saved_articles = relationship(
        "Article", 
        secondary="saved_articles",
        primaryjoin="Profile.id == saved_articles.c.profile_id",
        secondaryjoin="Article.id == saved_articles.c.article_id"
    )

    __table_args__ = {'extend_existing': True}

# Association table for saved articles
saved_articles = Table(
    "saved_articles",
    Base.metadata,
    Column("profile_id", String, ForeignKey("profiles.id"), primary_key=True),
    Column("article_id", String, ForeignKey("articles.id"), primary_key=True),
    extend_existing=True
)
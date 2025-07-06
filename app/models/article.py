from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base
import enum
import uuid

class ArticleStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    REVIEW = "REVIEW"
    PUBLISHED = "PUBLISHED"

class Article(Base):
    __tablename__ = "articles"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    slug = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False, index=True)
    subcategory = Column(String, index=True)
    written_by = Column(String, ForeignKey("users.id"), nullable=False)
    reviewed_by = Column(String, ForeignKey("users.id"), nullable=True)
    author = Column(String, nullable=False)  # This can be the author's name or username
    date = Column(String, nullable=False)  
    read_time = Column(String, nullable=False)
    image = Column(String, nullable=False)
    href = Column(String, nullable=False)
    content = Column(String, nullable=False)
    description = Column(String, nullable=False)
    is_premium = Column(Boolean, default=False)
    status = Column(Enum(ArticleStatus), default=ArticleStatus.DRAFT, nullable=False)
    caption = Column(String)
    quote = Column(String)
    quote_author = Column(String)
    tag = Column(String)
    no_of_readers = Column(Integer, default=0, nullable=False)

    written_by_user = relationship(
        "User",
        back_populates="articles",
        foreign_keys=[written_by]
    )

    reviewed_by_user = relationship(
        "User",
        back_populates="reviewed_articles",
        foreign_keys=[reviewed_by]
    )

    __table_args__ = {'extend_existing': True}

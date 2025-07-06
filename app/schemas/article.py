from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from .common import CamelModel

class ArticleStatus(str, Enum):
    DRAFT = "DRAFT"
    REVIEW = "REVIEW"
    PUBLISHED = "PUBLISHED"

class ArticleBase(CamelModel):
    slug: str
    title: str
    category: str
    subcategory: Optional[str] = None
    author: str  # Display name (e.g., full name or username)
    written_by: str  # User ID
    reviewed_by: Optional[str] = None
    date: str  # ISO 8601
    read_time: str
    image: str
    href: str
    content: str
    description: str
    is_premium: bool = False
    status: ArticleStatus = ArticleStatus.DRAFT
    caption: Optional[str] = None
    quote: Optional[str] = None
    quote_author: Optional[str] = None
    tag: Optional[str] = None
    no_of_readers: int = 0

class ArticleCreate(CamelModel):
    title: str
    category: str
    subcategory: Optional[str] = None
    date: str  # ISO 8601
    read_time: str
    image: str
    content: str
    description: str
    is_premium: bool = False
    caption: Optional[str] = None
    quote: Optional[str] = None
    quote_author: Optional[str] = None
    tag: Optional[str] = None

    # Optional fields generated/set by backend
    slug: Optional[str] = None
    href: Optional[str] = None
    written_by: Optional[str] = None
    reviewed_by: Optional[str] = None
    status: Optional[ArticleStatus] = ArticleStatus.DRAFT

class ArticleUpdate(CamelModel):
    slug: Optional[str] = None
    title: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    date: Optional[str] = None
    read_time: Optional[str] = None
    image: Optional[str] = None
    href: Optional[str] = None
    content: Optional[str] = None
    description: Optional[str] = None
    is_premium: Optional[bool] = None
    status: Optional[ArticleStatus] = None
    caption: Optional[str] = None
    quote: Optional[str] = None
    quote_author: Optional[str] = None
    tag: Optional[str] = None
    written_by: Optional[str] = None
    reviewed_by: Optional[str] = None

class ArticlePreview(CamelModel):
    id: str
    slug: str
    title: str
    category: str
    subcategory: Optional[str] = None
    date: str
    read_time: str
    image: str
    description: str
    is_premium: bool = False
    no_of_readers: int = 0

class Article(ArticlePreview):
    author: str  # Full name or display name
    written_by: str
    reviewed_by: Optional[str] = None
    href: str
    content: str
    caption: Optional[str] = None
    quote: Optional[str] = None
    quote_author: Optional[str] = None
    tag: Optional[str] = None
    status: ArticleStatus

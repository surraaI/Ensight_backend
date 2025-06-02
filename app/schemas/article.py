from pydantic import BaseModel, HttpUrl
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
    author: str
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

class ArticleCreate(ArticleBase):
    pass

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

class Article(ArticleBase):
    id: str
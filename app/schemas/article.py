from pydantic import BaseModel, UUID4, HttpUrl
from typing import Optional, List
from datetime import datetime

class ArticleBase(BaseModel):
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
    caption: Optional[str] = None
    quote: Optional[str] = None
    quote_author: Optional[str] = None
    tag: Optional[str] = None
    no_of_readers: int = 0

class ArticleCreate(ArticleBase):
    pass

class Article(ArticleBase):
    id: str

    class Config:
        orm_mode = True

class ReadingHistoryEntryBase(BaseModel):
    article_id: str
    progress: int

class ReadingHistoryEntryCreate(ReadingHistoryEntryBase):
    pass

class ReadingHistoryEntry(ReadingHistoryEntryBase):
    id: str
    article: Article

    class Config:
        orm_mode = True
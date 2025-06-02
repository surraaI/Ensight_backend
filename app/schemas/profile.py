from pydantic import EmailStr
from typing import Optional, List
from .common import CamelModel
from .article import Article

class ReadingHistoryEntry(CamelModel):
    article: Article
    progress: int

class ProfileBase(CamelModel):
    first_name: str
    last_name: str
    email: EmailStr
    avatar: Optional[str] = None
    created_at: str  # ISO 8601
    enable_personalization: bool = False
    track_reading_progress: bool = False
    content_update_notifications: bool = False
    topics: List[str] = []

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(CamelModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    avatar: Optional[str] = None
    enable_personalization: Optional[bool] = None
    track_reading_progress: Optional[bool] = None
    content_update_notifications: Optional[bool] = None
    topics: Optional[List[str]] = None

class Profile(ProfileBase):
    id: str
    saved_articles: List[Article] = []
    reading_history: List[ReadingHistoryEntry] = []
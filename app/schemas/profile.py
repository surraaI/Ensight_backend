from pydantic import EmailStr
from typing import Optional, List
from .common import CamelModel
from .article import Article
from app.models.user import Role
from datetime import datetime

class ReadingHistoryEntry(CamelModel):
    article: Article
    progress: int

class ProfileBase(CamelModel):
    first_name: str
    last_name: str
    email: EmailStr
    profile_image: Optional[str] = None
    created_at: Optional[str] = datetime.utcnow().isoformat()
    enable_personalization: bool = False
    track_reading_progress: bool = False
    content_update_notifications: bool = False
    topics: List[str] = []

class ProfileCreate(ProfileBase):
    password: str
    role: Role

class ProfileUpdate(CamelModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    profile_image: Optional[str] = None
    enable_personalization: Optional[bool] = None
    track_reading_progress: Optional[bool] = None
    content_update_notifications: Optional[bool] = None
    topics: Optional[List[str]] = None

class Profile(ProfileBase):
    id: str
    saved_articles: List[Article] = []
    reading_history: List[ReadingHistoryEntry] = []
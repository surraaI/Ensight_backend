from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class OriginalContentBase(BaseModel):
    title: str
    body: str
    is_premium: bool = False
    thumbnail_url: Optional[str] = None
    written_by: Optional[str] = None
    edited_by: Optional[str] = None
    approved_by: Optional[str] = None


class OriginalContentCreate(OriginalContentBase):
    pass


class OriginalContentUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    is_premium: Optional[bool] = None
    thumbnail_url: Optional[str] = None
    written_by: Optional[str] = None
    edited_by: Optional[str] = None
    approved_by: Optional[str] = None


class OriginalContentOut(OriginalContentBase):
    id: str
    status: str
    author_id: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime] = None
    published_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # for Pydantic v2

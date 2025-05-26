from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional
from .category import CategoryOut, SubcategoryOut 


class AggregatedNewsBase(BaseModel):
    title: str
    summary: str
    source: str
    url: Optional[HttpUrl] = None
    thumbnail_url: Optional[str] = None
    category_id: Optional[str] = None
    subcategory_id: Optional[str] = None


class AggregatedNewsCreate(AggregatedNewsBase):
    pass


class AggregatedNewsUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    source: Optional[str] = None
    url: Optional[HttpUrl] = None
    thumbnail_url: Optional[str] = None
    category_id: Optional[str] = None
    subcategory_id: Optional[str] = None


class AggregatedNewsOut(AggregatedNewsBase):
    id: str
    status: str
    written_by: Optional[str]
    edited_by: Optional[str]
    approved_by: Optional[str]
    category: Optional[CategoryOut] = None
    subcategory: Optional[SubcategoryOut] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    published_at: Optional[datetime] = None

    class Config:
        from_attributes = True
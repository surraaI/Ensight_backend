from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class AggregatedNewsBase(BaseModel):
    title: str
    summary: str
    source: str
    url: HttpUrl
    thumbnail_url: Optional[str]
    written_by: Optional[str]
    edited_by: Optional[str]
    approved_by: Optional[str]


class AggregatedNewsCreate(AggregatedNewsBase):
    pass

class AggregatedNewsOut(AggregatedNewsBase):
    id: str
    status: str
    created_at: datetime

    class Config:
        orm_mode = True

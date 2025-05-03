from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class OriginalContentBase(BaseModel):
    title: str
    body: str
    is_premium: bool = False
    thumbnail_url: Optional[str]
    written_by: Optional[str]
    edited_by: Optional[str]
    approved_by: Optional[str]


class OriginalContentCreate(OriginalContentBase):
    pass

class OriginalContentOut(OriginalContentBase):
    id: str
    status: str
    author_id: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True

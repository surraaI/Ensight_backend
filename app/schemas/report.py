from pydantic import BaseModel, UUID4, HttpUrl
from typing import Optional

class ReportBase(BaseModel):
    title: str
    description: str
    image: str
    published: str  # ISO 8601
    button_text: str
    button_link: str

class ReportCreate(ReportBase):
    pass

class Report(ReportBase):
    id: str

    class Config:
        orm_mode = True
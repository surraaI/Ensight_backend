from pydantic import BaseModel, UUID4, HttpUrl
from typing import Optional

class DataInsightBase(BaseModel):
    title: str
    description: str
    icon: str
    updated: str  # ISO 8601
    button_text: str
    button_link: str

class DataInsightCreate(DataInsightBase):
    pass

class DataInsight(DataInsightBase):
    id: str

    class Config:
        orm_mode = True
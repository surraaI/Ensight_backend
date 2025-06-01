from pydantic import BaseModel, UUID4, HttpUrl
from typing import Optional

class EventBase(BaseModel):
    date: str
    title: str
    button_text: str
    button_link: str

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: str

    class Config:
        orm_mode = True
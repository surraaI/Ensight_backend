from pydantic import BaseModel, UUID4, HttpUrl
from typing import Optional

class StartupBase(BaseModel):
    name: str
    description: str
    image: str
    href: str

class StartupCreate(StartupBase):
    pass

class Startup(StartupBase):
    id: str

    class Config:
        orm_mode = True
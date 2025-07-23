from pydantic import BaseModel, HttpUrl
from typing import Optional


class CorporateBase(BaseModel):
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    image: Optional[HttpUrl] = None
    profile_image: Optional[HttpUrl] = None
    name: Optional[str] = None
    role: Optional[str] = None
    born: Optional[str] = None
    education: Optional[str] = None
    mission: Optional[str] = None
    specialties: Optional[str] = None
    certifications: Optional[str] = None
    motto: Optional[str] = None
    founded: Optional[str] = None
    quote: Optional[str] = None

class CorporateCreate(CorporateBase):
    pass

class CorporateUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    image: Optional[HttpUrl] = None
    profile_image: Optional[HttpUrl] = None
    name: Optional[str] = None
    role: Optional[str] = None
    born: Optional[str] = None
    education: Optional[str] = None
    mission: Optional[str] = None
    specialties: Optional[str] = None
    certifications: Optional[str] = None
    motto: Optional[str] = None
    founded: Optional[str] = None
    quote: Optional[str] = None

class CorporateOut(CorporateBase):
    id: str
    created_at: str

    class Config:
        orm_mode = True

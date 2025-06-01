from pydantic import BaseModel, UUID4
from typing import List, Optional

class PlanBase(BaseModel):
    name: str
    price: str
    description: str
    features: List[str] = []
    is_highlighted: bool = False

class PlanCreate(PlanBase):
    pass

class Plan(PlanBase):
    id: str

    class Config:
        orm_mode = True
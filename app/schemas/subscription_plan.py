from pydantic import BaseModel, UUID4, HttpUrl
from typing import Union, List, Optional

class Price(BaseModel):
    monthly: Optional[str] = None
    annual: Optional[str] = None

class SubscriptionPlanBase(BaseModel):
    title: str
    description: str
    price: Union[str, Price]
    features: List[str] = []
    button_text: str
    button_link: str
    highlighted: bool = False

class SubscriptionPlanCreate(SubscriptionPlanBase):
    pass

class SubscriptionPlan(SubscriptionPlanBase):
    id: str

    class Config:
        orm_mode = True
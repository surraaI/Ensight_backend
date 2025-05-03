from pydantic import BaseModel
from typing import Optional

class EnterpriseAccountBase(BaseModel):
    name: str

class EnterpriseAccountCreate(EnterpriseAccountBase):
    pass

class EnterpriseAccountOut(EnterpriseAccountBase):
    id: str

    class Config:
        orm_mode = True

class EnterpriseUserBase(BaseModel):
    user_id: str
    account_id: str

class EnterpriseUserOut(EnterpriseUserBase):
    id: str

    class Config:
        orm_mode = True

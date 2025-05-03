from pydantic import BaseModel
from datetime import datetime

class APIKeyOut(BaseModel):
    id: str
    key: str
    is_active: bool
    created_at: datetime
    owner_id: str

    class Config:
        orm_mode = True

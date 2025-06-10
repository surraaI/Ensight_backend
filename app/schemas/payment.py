from datetime import datetime
from enum import Enum
from pydantic import BaseModel

class PaymentStatus(str, Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"

class PaymentSubmissionBase(BaseModel):
    plan_id: str
    screenshot_url: str

class PaymentSubmissionCreate(PaymentSubmissionBase):
    pass

class PaymentSubmission(PaymentSubmissionBase):
    id: str
    user_id: str
    status: PaymentStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
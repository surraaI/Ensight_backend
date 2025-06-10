# from sqlalchemy import Column, String, JSON, Boolean, ARRAY, ForeignKey, DateTime, Enum
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.orm import relationship
# from app.database import Base
# import uuid
# from datetime import datetime
# import enum

# class PaymentStatus(enum.Enum):
#     PENDING = "pending"
#     VERIFIED = "verified"
#     REJECTED = "rejected"

# class PaymentSubmission(Base):
#     __tablename__ = "payment_submissions"
    
#     id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
#     user_id = Column(String, ForeignKey('users.id'), nullable=False)
#     plan_id = Column(String, ForeignKey('subscription_plans.id'), nullable=False)
#     screenshot_url = Column(String, nullable=False)
#     status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
#     user = relationship("User", back_populates="payments")
#     plan = relationship("SubscriptionPlan")
from sqlalchemy import Column, String, JSON, Boolean, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid

class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(JSON, nullable=False)  # Store as JSON for string or {monthly, annual}
    features = Column(ARRAY(String), default=[])
    button_text = Column(String, nullable=False)
    button_link = Column(String, nullable=False)
    highlighted = Column(Boolean, default=False)

    __table_args__ = {'extend_existing': True}
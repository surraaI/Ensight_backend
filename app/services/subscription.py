from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.subscription_plan import SubscriptionPlan
from app.schemas.subscription_plan import SubscriptionPlanCreate, SubscriptionPlan
from uuid import uuid4

class SubscriptionService:
    @staticmethod
    def create_or_update_subscription(
        db: Session, 
        subscription_data: SubscriptionPlanCreate
    ) -> SubscriptionPlan:
        # Convert Pydantic model to dict
        data = subscription_data.dict()
        
        # If ID is provided, try to update existing subscription
        if "id" in data and data["id"]:
            subscription = db.get(SubscriptionPlan, data["id"])
            if subscription:
                # Update existing subscription
                for key, value in data.items():
                    if key != "id" and hasattr(subscription, key):
                        setattr(subscription, key, value)
                db.commit()
                db.refresh(subscription)
                return subscription
        
        # Create new subscription
        if "id" not in data or not data["id"]:
            data["id"] = str(uuid4())
        
        db_subscription = SubscriptionPlan(**data)
        db.add(db_subscription)
        db.commit()
        db.refresh(db_subscription)
        return db_subscription

    @staticmethod
    def get_subscription_plan(db: Session, plan_id: str) -> SubscriptionPlan:
        return db.get(SubscriptionPlan, plan_id)

    @staticmethod
    def get_all_subscription_plans(db: Session) -> list[SubscriptionPlan]:
        return db.execute(select(SubscriptionPlan)).scalars().all()

    @staticmethod
    def delete_subscription_plan(db: Session, plan_id: str) -> bool:
        subscription = db.get(SubscriptionPlan, plan_id)
        if not subscription:
            return False
        
        db.delete(subscription)
        db.commit()
        return True
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.subscription_plan import SubscriptionPlan
from app.schemas.subscription_plan import SubscriptionPlanCreate, SubscriptionPlan
from uuid import uuid4
from app.models.user import User
from datetime import datetime, timedelta

class SubscriptionService:
    @staticmethod
    def subscribe_user(
        db: Session,
        user_id: str,
        plan_id: str,
        duration: str = "monthly"  # "monthly" or "annual"
    ) -> User:
        # Get user
        user = db.execute(
            select(User).filter_by(id=user_id)
        ).scalar_one_or_none()
        
        if not user:
            raise ValueError("User not found")
        
        # Get plan
        plan = db.execute(
            select(SubscriptionPlan).filter_by(id=plan_id)
        ).scalar_one_or_none()
        
        if not plan:
            raise ValueError("Subscription plan not found")
        
        # Calculate subscription period
        start_date = datetime.utcnow()
        if duration == "annual":
            end_date = start_date + timedelta(days=365)
        else:  # monthly
            end_date = start_date + timedelta(days=30)
        
        # Update user subscription
        user.subscription_plan_id = plan_id
        user.subscription_start = start_date
        user.subscription_end = end_date
        
        # Upgrade role to SUBSCRIBER
        if user.role != "SUBSCRIBER":
            user.role = "SUBSCRIBER"
        
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_user_subscription_status(db: Session, user_id: str) -> dict:
        user = db.execute(
            select(User).filter_by(id=user_id)
        ).scalar_one_or_none()
        
        if not user or not user.subscription_end:
            return {"is_active": False}
        
        return {
            "is_active": user.subscription_end > datetime.utcnow(),
            "start": user.subscription_start,
            "end": user.subscription_end,
            "plan": user.subscription_plan
        }

    @staticmethod
    def cancel_subscription(db: Session, user_id: str) -> User:
        user = db.execute(
            select(User).filter_by(id=user_id)
        ).scalar_one_or_none()
        
        if not user:
            raise ValueError("User not found")
        
        # Downgrade role to FREE_USER
        if user.role == "SUBSCRIBER":
            user.role = "FREE_USER"
        
        # Clear subscription fields
        user.subscription_plan_id = None
        user.subscription_start = None
        user.subscription_end = None
        
        db.commit()
        db.refresh(user)
        return user
    
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
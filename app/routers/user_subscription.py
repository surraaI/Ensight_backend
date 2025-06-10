from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.subscription import SubscriptionService
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/user", tags=["user subscriptions"])

@router.post("/subscribe", status_code=status.HTTP_200_OK)
async def subscribe_user(
    plan_id: str,
    duration: str = "monthly",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Subscribe current user to a premium plan
    - duration: 'monthly' or 'annual'
    """
    try:
        user = SubscriptionService.subscribe_user(
            db, current_user.id, plan_id, duration
        )
        return {"message": "Subscription successful", "user": user}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/subscription", status_code=status.HTTP_200_OK)
async def get_user_subscription_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's subscription status"""
    return SubscriptionService.get_user_subscription_status(db, current_user.id)

@router.post("/subscription/cancel", status_code=status.HTTP_200_OK)
async def cancel_subscription(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cancel current user's subscription"""
    try:
        user = SubscriptionService.cancel_subscription(db, current_user.id)
        return {"message": "Subscription cancelled", "user": user}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
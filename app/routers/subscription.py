from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.subscription import SubscriptionService
from app.schemas.subscription_plan import (
    SubscriptionPlanCreate,
    SubscriptionPlan
)
from app.dependencies import get_current_user, require_role
from app.models.user import User, Role

router = APIRouter(prefix="/subscribe", tags=["subscription"])

@router.post("/", 
             response_model=SubscriptionPlan,
             status_code=status.HTTP_201_CREATED)
async def create_or_update_subscription(
    subscription: SubscriptionPlanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([Role.ADMIN, Role.SUPERADMIN]))
):
    """
    Create or update a subscription plan
    - If ID is provided and exists: updates the existing plan
    - If ID is not provided or doesn't exist: creates a new plan
    Requires ADMIN or SUPERADMIN role
    """
    return SubscriptionService.create_or_update_subscription(db, subscription)

@router.get("/", response_model=list[SubscriptionPlan])
async def get_all_subscription_plans(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all available subscription plans"""
    return SubscriptionService.get_all_subscription_plans(db)

@router.get("/{plan_id}", response_model=SubscriptionPlan)
async def get_subscription_plan(
    plan_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific subscription plan by ID"""
    plan = SubscriptionService.get_subscription_plan(db, plan_id)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription plan not found"
        )
    return plan

@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subscription_plan(
    plan_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([Role.ADMIN, Role.SUPERADMIN]))
):
    """Delete a subscription plan (ADMIN or SUPERADMIN only)"""
    if not SubscriptionService.delete_subscription_plan(db, plan_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription plan not found"
        )
    return
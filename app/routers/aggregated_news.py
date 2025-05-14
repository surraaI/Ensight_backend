from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.aggregated_news import AggregatedNewsCreate, AggregatedNewsUpdate, AggregatedNewsOut
from app.services.aggregated_news_service import (
    create_news, update_news, approve_news
)
from app.dependencies import get_db, get_current_user
from app.models.user import User, Role

router = APIRouter(prefix="/aggregated-news", tags=["Aggregated News"])


@router.post("/", response_model=AggregatedNewsOut)
def create_aggregated_news(
    news_data: AggregatedNewsCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in [Role.WRITER, Role.EDITOR, Role.ADMIN]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return create_news(db, news_data, current_user)


@router.put("/{news_id}", response_model=AggregatedNewsOut)
def update_aggregated_news(
    news_id: str,
    news_data: AggregatedNewsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_news(db, news_id, news_data, current_user)


@router.post("/{news_id}/approve", response_model=AggregatedNewsOut)
def approve_aggregated_news(
    news_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can approve news")
    return approve_news(db, news_id, current_user)

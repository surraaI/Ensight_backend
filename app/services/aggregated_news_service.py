from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.aggregated_news import AggregatedNews, NewsStatus
from app.models.user import User
from app.schemas.aggregated_news import AggregatedNewsCreate, AggregatedNewsUpdate
from uuid import uuid4
from datetime import datetime


def create_news(db: Session, news_data: AggregatedNewsCreate, current_user: User):
    news = AggregatedNews(
        id=str(uuid4()),
        title=news_data.title,
        summary=news_data.summary,
        source=news_data.source,
        category_id=news_data.category_id,
        subcategory_id=news_data.subcategory_id,
        image_url=news_data.image_url,
        status=NewsStatus.DRAFT,
        written_by_id=current_user.id,
        created_at=datetime.utcnow()
    )
    db.add(news)
    db.commit()
    db.refresh(news)
    return news


def update_news(db: Session, news_id: str, news_data: AggregatedNewsUpdate, current_user: User):
    news = db.query(AggregatedNews).filter_by(id=news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="News not found")

    if news.status == NewsStatus.PUBLISHED:
        raise HTTPException(status_code=403, detail="Cannot edit published news")

    if current_user.role not in ["EDITOR", "ADMIN"] and news.written_by_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")

    for key, value in news_data.dict(exclude_unset=True).items():
        setattr(news, key, value)
    news.edited_by_id = current_user.id
    news.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(news)
    return news


def approve_news(db: Session, news_id: str, current_user: User):
    news = db.query(AggregatedNews).filter_by(id=news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="News not found")

    news.status = NewsStatus.PUBLISHED
    news.approved_by_id = current_user.id
    news.published_at = datetime.utcnow()

    db.commit()
    db.refresh(news)
    return news

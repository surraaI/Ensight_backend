from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.original_content import OriginalContent, ContentStatus
from app.models.user import User
from app.schemas.original_content import OriginalContentCreate, OriginalContentUpdate
from uuid import uuid4
from datetime import datetime


def create_original_content(db: Session, content_data: OriginalContentCreate, current_user: User):
    content = OriginalContent(
        id=str(uuid4()),
        title=content_data.title,
        body=content_data.body,
        category_id=content_data.category_id,
        subcategory_id=content_data.subcategory_id,
        image_url=content_data.image_url,
        is_premium=content_data.is_premium,
        status=ContentStatus.DRAFT,
        written_by_id=current_user.id,
        created_at=datetime.utcnow()
    )
    db.add(content)
    db.commit()
    db.refresh(content)
    return content


def update_original_content(db: Session, content_id: str, content_data: OriginalContentUpdate, current_user: User):
    content = db.query(OriginalContent).filter_by(id=content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    if content.status == ContentStatus.PUBLISHED:
        raise HTTPException(status_code=403, detail="Cannot edit published content")

    if current_user.role not in ["EDITOR", "ADMIN"] and content.written_by_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")

    for key, value in content_data.dict(exclude_unset=True).items():
        setattr(content, key, value)
    content.edited_by_id = current_user.id
    content.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(content)
    return content


def approve_original_content(db: Session, content_id: str, current_user: User):
    content = db.query(OriginalContent).filter_by(id=content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    content.status = ContentStatus.PUBLISHED
    content.approved_by_id = current_user.id
    content.published_at = datetime.utcnow()

    db.commit()
    db.refresh(content)
    return content

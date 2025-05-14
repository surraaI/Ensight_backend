from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.original_content import OriginalContentCreate, OriginalContentUpdate, OriginalContentOut
from app.services.original_content_service import (
    create_original_content, update_original_content, approve_original_content
)
from app.dependencies import get_db, get_current_user
from app.models.user import User, Role

router = APIRouter(prefix="/original-content", tags=["Original Content"])


@router.post("/", response_model=OriginalContentOut)
def create_content(
    content_data: OriginalContentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in [Role.WRITER, Role.EDITOR, Role.ADMIN]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return create_original_content(db, content_data, current_user)


@router.put("/{content_id}", response_model=OriginalContentOut)
def update_content(
    content_id: str,
    content_data: OriginalContentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_original_content(db, content_id, content_data, current_user)


@router.post("/{content_id}/approve", response_model=OriginalContentOut)
def approve_content(
    content_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can approve content")
    return approve_original_content(db, content_id, current_user)

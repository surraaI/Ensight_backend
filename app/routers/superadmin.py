from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.schemas.user import UserCreate, UserOut
from app.services.superadmin_service import create_user_with_role
from app.models.user import Role, User

router = APIRouter(prefix="/superadmin", tags=["Superadmin"])

@router.post("/create-user", response_model=UserOut)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Only superadmins can create users")
    
    return create_user_with_role(db, user_data)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.schemas.user import UserCreateByAdmin, UserOut
from app.services.superadmin_service import create_user_by_admin
from app.models.user import Role, User

router = APIRouter(prefix="/superadmin", tags=["Superadmin"])

@router.post("/create-user", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreateByAdmin,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Only allow SUPERADMIN to create users
    if current_user.role != Role.SUPERADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only superadmins can create privileged users"
        )
    
    return create_user_by_admin(db, user_data)
from fastapi import APIRouter, Depends
from jose import jwt
from app.core.config import settings
from app.dependencies import get_current_user

router = APIRouter()

@router.get("/debug/token")
def debug_token(current_user: User = Depends(get_current_user)):
    return {
        "user_id": current_user.id,
        "email": current_user.email,
        "role": current_user.role
    }
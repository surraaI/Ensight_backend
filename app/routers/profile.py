from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.profile_service import get_profile, update_profile, delete_profile
from app.schemas.profile import Profile, ProfileUpdate
from app.dependencies import get_current_user

router = APIRouter()

@router.get("/{user_id}", response_model=Profile)
def read_profile(
    user_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Ensure users can only access their own profile
    if current_user["id"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this profile")
    
    profile = get_profile(db, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.patch("/{user_id}", response_model=Profile)
def update_user_profile(
    user_id: str,
    profile_data: ProfileUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user["id"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this profile")
    
    profile = update_profile(db, user_id, profile_data)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.delete("/{user_id}")
def delete_user_profile(
    user_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user["id"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this profile")
    
    if not delete_profile(db, user_id):
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"message": "Profile deleted successfully"}
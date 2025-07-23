from fastapi import APIRouter, Depends, HTTPException, status, Body, Form, File
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.services.profile_service import (
    get_profile, update_profile, delete_profile,
    add_saved_article, get_saved_articles, remove_saved_article,
    get_all_profiles, create_user_with_role
)
from app.schemas.profile import Profile, ProfileUpdate, ProfileCreate
from app.dependencies import get_current_user, require_role
from app.models.user import Role, User
from app.schemas.article import Article
from datetime import datetime


router = APIRouter(prefix="/profiles", tags=["Profiles"])

import cloudinary.uploader
from fastapi import UploadFile

def upload_profile_image_to_cloudinary(file: UploadFile) -> str:
    result = cloudinary.uploader.upload(file.file, folder="profile_images")
    return result.get("secure_url")

@router.get("/{user_id}", response_model=Profile)
def read_profile(
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        role = Role(current_user.role)
    except ValueError:
        raise HTTPException(status_code=403, detail="Invalid role")

    if role != Role.SUPERADMIN and str(current_user.id) != str(user_id):
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
    if current_user.id != user_id:
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
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this profile")
    
    if not delete_profile(db, user_id):
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"message": "Profile deleted successfully"}

@router.post("/{user_id}/saved_articles", response_model=Article, status_code=status.HTTP_201_CREATED)
def save_article_for_user(
    user_id: str,
    article_id: str = Body(..., embed=True),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to save articles for this user")
    
    article = add_saved_article(db, user_id, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found or already saved")
    return article

@router.get("/{user_id}/saved_articles", response_model=list[Article])
def get_user_saved_articles(
    user_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to view saved articles")
    
    return get_saved_articles(db, user_id)

@router.delete("/{user_id}/saved_articles/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_saved_article_for_user(
    user_id: str,
    article_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to modify saved articles")
    
    if not remove_saved_article(db, user_id, article_id):
        raise HTTPException(status_code=404, detail="Saved article not found")
    

@router.get("/", response_model=List[Profile])
def get_all_user_profiles(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([Role.SUPERADMIN]))
):
    return get_all_profiles(db)

@router.post("/", response_model=Profile, status_code=status.HTTP_201_CREATED)
def create_profile_with_role(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role: Role = Form(...),
    profile_image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([Role.SUPERADMIN]))
):
    image_url = None
    if profile_image:
        try:
            image_url = upload_profile_image_to_cloudinary(profile_image)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Image upload failed: {str(e)}")

    profile_data = ProfileCreate(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        role=role,
        created_at=datetime.utcnow().isoformat()
    )

    return create_user_with_role(db, profile_data, profile_image_path=image_url)
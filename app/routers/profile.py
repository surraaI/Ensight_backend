from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.profile_service import get_profile, update_profile, delete_profile, add_saved_article, get_saved_articles,remove_saved_article
from app.schemas.profile import Profile, ProfileUpdate
from app.dependencies import get_current_user
from app.schemas.article import Article 


router = APIRouter(prefix="/Profile", tags=["Profiles"])

@router.get("/{user_id}", response_model=Profile)
def read_profile(
    user_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Ensure users can only access their own profile
    if current_user.id != user_id:
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
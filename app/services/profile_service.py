from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from typing import Optional, List
from app.models.profile import Profile as ProfileModel, saved_articles
from app.schemas.profile import Profile, ProfileUpdate, ProfileCreate
from app.models.user import User
from datetime import datetime
from app.models.article import Article as ArticleModel
from app.models.user import Role
from passlib.context import CryptContext
import uuid



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_profile(db: Session, user_id: str) -> ProfileModel:
    profile = db.query(ProfileModel).filter(ProfileModel.user_id == user_id).first()
    if not profile:
        # Create a default profile if not exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
            
        profile = ProfileModel(
            user_id=user_id,
            first_name="New",
            last_name="User",
            email=user.email,
            created_at=datetime.utcnow().isoformat()
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile

def update_profile(db: Session, user_id: str, profile_data: ProfileUpdate) -> ProfileModel:
    profile = get_profile(db, user_id)
    if not profile:
        return None
    
    update_data = profile_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(profile, key, value)
    
    db.commit()
    db.refresh(profile)
    return profile

def delete_profile(db: Session, user_id: str) -> bool:
    profile = db.query(ProfileModel).filter(ProfileModel.user_id == user_id).first()
    if not profile:
        return False
    
    db.delete(profile)
    db.commit()
    return True

def add_saved_article(db: Session, user_id: str, article_id: str) -> ArticleModel:
    profile = get_profile(db, user_id)
    if not profile:
        return None
    
    # Check if article exists
    article = db.query(ArticleModel).filter(ArticleModel.id == article_id).first()
    if not article:
        return None
    
    # Check if already saved
    if db.query(saved_articles).filter(
        saved_articles.c.profile_id == profile.id,
        saved_articles.c.article_id == article_id
    ).first():
        return None
    
    # Add to saved articles
    stmt = saved_articles.insert().values(profile_id=profile.id, article_id=article_id)
    db.execute(stmt)
    db.commit()
    return article

def get_saved_articles(db: Session, user_id: str) -> list[ArticleModel]:
    profile = get_profile(db, user_id)
    if not profile:
        return []
    
    return profile.saved_articles

def remove_saved_article(db: Session, user_id: str, article_id: str) -> bool:
    profile = get_profile(db, user_id)
    if not profile:
        return False
    
    # Check if the article is saved
    stmt = saved_articles.delete().where(
        (saved_articles.c.profile_id == profile.id) &
        (saved_articles.c.article_id == article_id)
    )
    result = db.execute(stmt)
    db.commit()
    return result.rowcount > 0

def get_all_profiles(db: Session) -> list[ProfileModel]:
    return db.query(ProfileModel).all()


def create_user_with_role(
    db: Session, 
    profile_data: ProfileCreate, 
    profile_image_path: Optional[str] = None
) -> ProfileModel:
    # Check for valid role
    role = profile_data.role.upper()
    if role not in [r.value for r in Role]:
        # Changed to HTTPException
        raise HTTPException(
            status_code=400,
            detail=f"Invalid role. Allowed: {', '.join([r.value for r in Role])}"
        )

    # Check for duplicate email
    if db.query(User).filter(User.email == profile_data.email).first():
        raise HTTPException(status_code=400, detail="Email already exists.")

    # Create user
    user = User(
        id=str(uuid.uuid4()),
        email=profile_data.email,
        hashed_password=pwd_context.hash(profile_data.password),
        role=Role.ADMIN if role == "ADMIN" else Role.FREE_USER if role == "FREE_USER" else Role.EDITOR if role == "EDITOR" else Role.WRITER
    )
    db.add(user)
    db.commit()

    # Create associated profile
    profile = ProfileModel(
        user_id=user.id,
        first_name=profile_data.first_name,
        last_name=profile_data.last_name,
        email=profile_data.email,
        profile_image=profile_image_path,
        created_at=datetime.utcnow().isoformat()
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

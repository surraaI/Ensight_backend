from sqlalchemy.orm import Session
from app.models.profile import Profile as ProfileModel
from app.schemas.profile import Profile, ProfileUpdate
from app.models.user import User
from datetime import datetime

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
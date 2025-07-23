from pydantic import HttpUrl
from sqlalchemy.orm import Session
from app.models.corporate import Corporate
from app.schemas.corporate import CorporateCreate, CorporateUpdate

class CorporateService:
    @staticmethod
    def create_corporate(db: Session, data: CorporateCreate):
        payload = data.dict()
        for key in ["image", "profile_image"]:
            if isinstance(payload.get(key), HttpUrl):
                payload[key] = str(payload[key])

        corp = Corporate(**payload)
        db.add(corp)
        db.commit()
        db.refresh(corp)
        return corp

    @staticmethod
    def update_corporate(db: Session, id: str, updates: CorporateUpdate):
        corp = db.query(Corporate).filter(Corporate.id == id).first()
        if not corp:
            return None

        update_data = updates.dict(exclude_unset=True)
        for field in ["image", "profile_image"]:
            if isinstance(update_data.get(field), HttpUrl):
                update_data[field] = str(update_data[field])

        for key, value in update_data.items():
            setattr(corp, key, value)

        db.commit()
        db.refresh(corp)
        return corp


    @staticmethod
    def delete_corporate(db: Session, id: str):
        corp = db.query(Corporate).filter(Corporate.id == id).first()
        if not corp:
            return False
        db.delete(corp)
        db.commit()
        return True

    @staticmethod
    def get_corporate_by_id(db: Session, id: str):
        return db.query(Corporate).filter(Corporate.id == id).first()

    @staticmethod
    def get_all_corporates(db: Session):
        return db.query(Corporate).order_by(Corporate.title.asc()).all()

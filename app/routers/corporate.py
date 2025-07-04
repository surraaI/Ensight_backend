from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.corporate import CorporateCreate, CorporateUpdate, CorporateOut
from app.services.corporate import CorporateService
from app.core.cloudinary_config import cloudinary
import cloudinary.uploader

router = APIRouter(prefix="/api/corporate", tags=["corporate"])

@router.post("/", response_model=CorporateOut, status_code=status.HTTP_201_CREATED)
def create_corporate(data: CorporateCreate, db: Session = Depends(get_db)):
    return CorporateService.create_corporate(db, data)

@router.put("/{id}", response_model=CorporateOut)
def update_corporate(id: str, data: CorporateUpdate, db: Session = Depends(get_db)):
    updated = CorporateService.update_corporate(db, id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Corporate record not found")
    return updated

@router.delete("/{id}")
def delete_corporate(id: str, db: Session = Depends(get_db)):
    success = CorporateService.delete_corporate(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Corporate record not found")
    return {"detail": "Deleted successfully"}

@router.get("/", response_model=List[CorporateOut])
def get_all_corporates(db: Session = Depends(get_db)):
    return CorporateService.get_all_corporates(db)

@router.get("/{id}", response_model=CorporateOut)
def get_corporate_by_id(id: str, db: Session = Depends(get_db)):
    corp = CorporateService.get_corporate_by_id(db, id)
    if not corp:
        raise HTTPException(status_code=404, detail="Corporate record not found")
    return corp

@router.post("/upload")
def upload_image(file: UploadFile = File(...)):
    try:
        result = cloudinary.uploader.upload(file.file, folder="corporate")
        return {"image_url": result["secure_url"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

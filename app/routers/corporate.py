from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas.corporate import CorporateCreate, CorporateUpdate, CorporateOut
from app.services.corporate import CorporateService
from app.core.cloudinary_config import cloudinary
from app.dependencies import require_role
from app.models.user import Role, User
from datetime import datetime
import cloudinary.uploader

router = APIRouter(prefix="/corporate", tags=["corporate"])

ALLOWED_ROLES = [Role.SUPERADMIN, Role.ADMIN, Role.EDITOR, Role.WRITER]

@router.post("/", response_model=CorporateOut, status_code=status.HTTP_201_CREATED)
def create_corporate(
    title: str = Form(...),
    description: Optional[str] = Form(None),
    content: Optional[str] = Form(None),
    name: Optional[str] = Form(None),
    role: Optional[str] = Form(None),
    born: Optional[str] = Form(None),
    education: Optional[str] = Form(None),
    mission: Optional[str] = Form(None),
    specialties: Optional[str] = Form(None),
    certifications: Optional[str] = Form(None),
    motto: Optional[str] = Form(None),
    founded: Optional[str] = Form(None),
    quote: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    profile_image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(ALLOWED_ROLES))
):
    image_url = None
    profile_image_url = None

    if image:
        image_url = cloudinary.uploader.upload(image.file, folder="corporate")["secure_url"]
    if profile_image:
        profile_image_url = cloudinary.uploader.upload(profile_image.file, folder="corporate")["secure_url"]

    payload = CorporateCreate(
        title=title,
        description=description,
        content=content,
        image=image_url,
        profile_image=profile_image_url,
        name=name,
        role=role,
        born=born,
        education=education,
        mission=mission,
        specialties=specialties,
        certifications=certifications,
        motto=motto,
        founded=founded,
        quote=quote,
        created_at=datetime.utcnow().isoformat()
    )
    return CorporateService.create_corporate(db, payload)

@router.patch("/{id}", response_model=CorporateOut)
def partial_update_corporate(
    id: str,
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    content: Optional[str] = Form(None),
    name: Optional[str] = Form(None),
    role: Optional[str] = Form(None),
    born: Optional[str] = Form(None),
    education: Optional[str] = Form(None),
    mission: Optional[str] = Form(None),
    specialties: Optional[str] = Form(None),
    certifications: Optional[str] = Form(None),
    motto: Optional[str] = Form(None),
    founded: Optional[str] = Form(None),
    quote: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    profile_image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(ALLOWED_ROLES))
):
    image_url = None
    profile_image_url = None

    if image:
        image_url = cloudinary.uploader.upload(image.file, folder="corporate")["secure_url"]
    if profile_image:
        profile_image_url = cloudinary.uploader.upload(profile_image.file, folder="corporate")["secure_url"]

    updates = {
        "title": title,
        "description": description,
        "content": content,
        "name": name,
        "role": role,
        "born": born,
        "education": education,
        "mission": mission,
        "specialties": specialties,
        "certifications": certifications,
        "motto": motto,
        "founded": founded,
        "quote": quote,
        "image": image_url,
        "profile_image": profile_image_url,
    }

    updates = {k: v for k, v in updates.items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="No fields provided for update.")

    update_obj = CorporateUpdate(**updates)
    updated = CorporateService.update_corporate(db, id, update_obj)
    if not updated:
        raise HTTPException(status_code=404, detail="Corporate record not found")
    return updated

@router.delete("/{id}")
def delete_corporate(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(ALLOWED_ROLES))
):
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

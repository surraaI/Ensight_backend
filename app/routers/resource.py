from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.resource import ResourceService
from app.schemas.resources import (
    Resources,
    GetResourcesByTypeResponse,
    GetResourceBySlugResponse
)
from app.dependencies import get_current_user
from typing import Union, Optional
from app.models.user import User
from fastapi import Form, File, UploadFile
from app.dependencies import require_role

router = APIRouter(prefix="/resources", tags=["resources"])

@router.post("/", response_model=Resources)
async def create_resources_page(
    title: str = Form(...),
    description: str = Form(...),
    featured_insight_id: str = Form(...),
    report_ids: Optional[str] = Form(""),
    data_insight_ids: Optional[str] = Form(""),
    event_ids: Optional[str] = Form(""),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["SUPERADMIN", "ADMIN", "EDITOR", "WRITER"]))
):
    return ResourceService.create_resources(
        db=db,
        title=title,
        description=description,
        featured_insight_id=featured_insight_id,
        report_ids=report_ids,
        data_insight_ids=data_insight_ids,
        event_ids=event_ids,
    )

@router.patch("/", response_model=Resources)
async def update_resources_page(
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    featured_insight_id: Optional[str] = Form(None),
    report_ids: Optional[str] = Form(None),
    data_insight_ids: Optional[str] = Form(None),
    event_ids: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["SUPERADMIN", "ADMIN", "EDITOR", "WRITER"]))
):
    return ResourceService.update_resources(
        db=db,
        title=title,
        description=description,
        featured_insight_id=featured_insight_id,
        report_ids=report_ids,
        data_insight_ids=data_insight_ids,
        event_ids=event_ids,
    )
    
@router.get("/type", response_model=GetResourcesByTypeResponse)
async def get_resources_by_type(
    type: str = Query(..., 
                     description="Resource type: report, dataInsight, event"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resources = ResourceService.get_resources_by_type(db, type)
    if resources is None:
        raise HTTPException(
            status_code=400, 
            detail="Invalid resource type. Valid types: report, dataInsight, event"
        )
    if not resources:
        # Return empty list instead of 404 for consistency
        return []
    return resources

@router.get("/type/slug", response_model=GetResourceBySlugResponse)
async def get_resource_by_slug(
    type: str = Query(..., 
                     description="Resource type: report, dataInsight, event"),
    slug: str = Query(..., description="Resource slug identifier"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resource = ResourceService.get_resource_by_slug(db, type, slug)
    if not resource:
        raise HTTPException(
            status_code=404, 
            detail=f"Resource not found with type '{type}' and slug '{slug}'"
        )
    return resource

@router.get("/", response_model=Resources)
async def get_resources(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get the main resources page configuration"""
    resources = ResourceService.get_resources(db)
    if not resources:
        raise HTTPException(
            status_code=404, 
            detail="Resources do not found. Please create it first."
        )
    return resources
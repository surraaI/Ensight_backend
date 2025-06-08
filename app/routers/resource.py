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
from typing import Union
from app.models.user import User

router = APIRouter(prefix="/resources", tags=["resources"])

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
async def get_resources_page(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get the main resources page configuration"""
    return ResourceService.get_resources_page(db)
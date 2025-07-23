from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.resources import Report, DataInsight, Event
from app.schemas.resources import (
    ReportBase, 
    DataInsightBase, 
    EventBase
)
from app.models.resources import Resources 
from fastapi import HTTPException
from typing import List
import json

class ResourceService:
    
    @staticmethod
    def create_resources(db: Session, title, description, featured_insight_id, report_ids, data_insight_ids, event_ids):
        resources = db.query(Resources).first()
        if resources:
            raise HTTPException(status_code=400, detail="Resources already exist")

        resource = Resources(
            title=title,
            description=description,
            featured_insight_id=featured_insight_id,
            report_ids=json.loads(report_ids or "[]"),
            data_insight_ids=json.loads(data_insight_ids or "[]"),
            event_ids=json.loads(event_ids or "[]"),
        )
        db.add(resource)
        db.commit()
        db.refresh(resource)
        return resource

    @staticmethod
    def update_resources(db: Session, title, description, featured_insight_id, report_ids, data_insight_ids, event_ids):
        resources = db.query(Resources).first()
        if not resources:
            raise HTTPException(status_code=404, detail="Resources not found")

        if title is not None:
            resources.title = title
        if description is not None:
            resources.description = description
        if featured_insight_id is not None:
            resources.featured_insight_id = featured_insight_id
        if report_ids is not None:
            resources.report_ids = json.loads(report_ids or "[]")
        if data_insight_ids is not None:
            resources.data_insight_ids = json.loads(data_insight_ids or "[]")
        if event_ids is not None:
            resources.event_ids = json.loads(event_ids or "[]")

        db.commit()
        db.refresh(resources)
        return resources
    
    @staticmethod
    def get_resources_by_type(db: Session, resource_type: str):
        if resource_type == "report":
            results = db.execute(select(Report)).scalars().all()
            return [ReportBase.from_orm(r) for r in results]
        elif resource_type == "dataInsight":
            results = db.execute(select(DataInsight)).scalars().all()
            return [DataInsightBase.from_orm(r) for r in results]
        elif resource_type == "event":
            results = db.execute(select(Event)).scalars().all()
            return [EventBase.from_orm(r) for r in results]
        return None

    @staticmethod
    def get_resource_by_slug(db: Session, resource_type: str, slug: str):
        if resource_type == "report":
            result = db.execute(select(Report).filter_by(slug=slug)).scalar_one_or_none()
            return ReportBase.from_orm(result) if result else None
        elif resource_type == "dataInsight":
            result = db.execute(select(DataInsight).filter_by(slug=slug)).scalar_one_or_none()
            return DataInsightBase.from_orm(result) if result else None
        elif resource_type == "event":
            result = db.execute(select(Event).filter_by(slug=slug)).scalar_one_or_none()
            return EventBase.from_orm(result) if result else None
        return None

    @staticmethod
    def get_resources_page(db: Session):
        # Get the main resources page configuration
        resources = db.execute(select(Resources)).scalar_one_or_none()
        if not resources:
            # Create default if none exists
            resources = Resources(
                title="Ensight Intelligence Hub",
                description="Your hub for reports, data insights, and events",
                featured_insight_id=""
            )
            db.add(resources)
            db.commit()
            db.refresh(resources)
        return resources
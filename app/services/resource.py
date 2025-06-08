from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.resources import Report, DataInsight, Event
from app.schemas.resources import (
    ReportBase, 
    DataInsightBase, 
    EventBase
)

class ResourceService:
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
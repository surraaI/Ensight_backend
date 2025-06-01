from pydantic import BaseModel, UUID4
from typing import List
from .article import Article
from .report import Report
from .data_insight import DataInsight
from .event import Event

class ResourcesBase(BaseModel):
    title: str
    description: str
    featured_insight_id: str
    report_ids: List[str] = []
    data_insight_ids: List[str] = []
    event_ids: List[str] = []

class ResourcesCreate(ResourcesBase):
    pass

class Resources(ResourcesBase):
    id: str
    featured_insight: Article
    reports: List[Report] = []
    data_insights: List[DataInsight] = []
    events: List[Event] = []

    class Config:
        orm_mode = True
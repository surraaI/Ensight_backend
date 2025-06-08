from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Union
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

class ReportBase(BaseModel):
    id: str
    title: str
    description: str
    image: str
    published: str  # ISO 8601 string
    buttonText: str = Field(..., alias="button_text")
    buttonLink: str = Field(..., alias="button_link")
    slug: str

    class Config:
        allow_population_by_field_name = True

class DataInsightBase(BaseModel):
    id: str
    title: str
    description: str
    icon: str
    updated: str  # ISO 8601 string
    buttonText: str = Field(..., alias="button_text")
    buttonLink: str = Field(..., alias="button_link")
    slug: str

    class Config:
        allow_population_by_field_name = True

class EventBase(BaseModel):
    id: str
    date: str
    title: str
    buttonText: str = Field(..., alias="button_text")
    buttonLink: str = Field(..., alias="button_link")
    slug: str

    class Config:
        allow_population_by_field_name = True

# Union types for responses
ResourceType = Union[ReportBase, DataInsightBase, EventBase]
GetResourcesByTypeResponse = List[ResourceType]
GetResourceBySlugResponse = ResourceType
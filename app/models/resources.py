from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

# Association tables
resource_reports = Table(
    "resource_reports",
    Base.metadata,
    Column("resources_id", String, ForeignKey("resources.id")),
    Column("report_id", String, ForeignKey("reports.id")),
    extend_existing=True
)

resource_data_insights = Table(
    "resource_data_insights",
    Base.metadata,
    Column("resources_id", String, ForeignKey("resources.id")),
    Column("data_insight_id", String, ForeignKey("data_insights.id")),
    extend_existing=True
)

resource_events = Table(
    "resource_events",
    Base.metadata,
    Column("resources_id", String, ForeignKey("resources.id")),
    Column("event_id", String, ForeignKey("events.id")),
    extend_existing=True
)

class Resources(Base):
    __tablename__ = "resources"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    featured_insight_id = Column(String, ForeignKey("articles.id"), nullable=True)
    report_ids = Column(ARRAY(String), default=[])
    data_insight_ids = Column(ARRAY(String), default=[])
    event_ids = Column(ARRAY(String), default=[])

    featured_insight = relationship("Article")
    reports = relationship("Report", secondary=resource_reports)
    data_insights = relationship("DataInsight", secondary=resource_data_insights)
    events = relationship("Event", secondary=resource_events)

class Report(Base):
    __tablename__ = "reports"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    image = Column(String, nullable=False)
    published = Column(String, nullable=False)  # Stored as ISO string
    button_text = Column(String, nullable=False)
    button_link = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)  # Added slug field

class DataInsight(Base):
    __tablename__ = "data_insights"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    icon = Column(String, nullable=False)
    updated = Column(String, nullable=False)  # Stored as ISO string
    button_text = Column(String, nullable=False)
    button_link = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)  # Added slug field

class Event(Base):
    __tablename__ = "events"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    date = Column(String, nullable=False)  # Stored as string
    title = Column(String, nullable=False)
    button_text = Column(String, nullable=False)
    button_link = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)  # Added slug field
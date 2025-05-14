from sqlalchemy import Column, String, ForeignKey
from app.database import Base
import uuid

class Category(Base):
    __tablename__ = "categories"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, unique=True)

class Subcategory(Base):
    __tablename__ = "subcategories"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, unique=True)
    category_id = Column(String, ForeignKey("categories.id"), nullable=True)

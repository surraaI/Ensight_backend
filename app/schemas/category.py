# app/schemas/category.py

from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    id: str

    class Config:
        from_attributes = True


class SubcategoryBase(BaseModel):
    name: str
    category_id: Optional[str]

class SubcategoryCreate(SubcategoryBase):
    pass

class SubcategoryOut(SubcategoryBase):
    id: str

    class Config:
        from_attributes = True

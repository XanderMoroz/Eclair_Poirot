from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.sweets.models import Category


class SweetCreate(BaseModel):
    """Validation scheme to create sweet"""
    title: str = "Название десерта"
    description: str = "Описание десерта"
    price: int = 123


class SweetResponse(BaseModel):
    """Validation scheme to response sweet"""
    id: int
    user_id: int
    title: str
    description: str
    price: int
    created_at: datetime
    categories: List[Category] | None


class CategoryCreate(BaseModel):
    """Validation scheme to create category"""
    title: str = "Торт Печенье Эклер"


class CategoryResponse(BaseModel):
    """Validation scheme to response category"""
    id: int
    title: str
    # sweets: List[Sweet]


class SweetCategoryCreate(BaseModel):
    """Validation scheme to add sweet to category"""
    sweet_id: int = "Numeric Value Required"
    category_id: int = "Numeric Value Required"


class SweetCategoryResponse(BaseModel):
    """Validation scheme to response to sweet in category"""
    sweet_id: int
    category_id: int
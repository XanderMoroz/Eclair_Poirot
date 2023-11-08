from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.sweets.models import Category, Ingredient


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
    ingredients: List[Ingredient] | None


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
    sweet_id: int
    category_id: int


class SweetCategoryResponse(BaseModel):
    """Validation scheme to response to sweet in category"""
    sweet_id: int
    category_id: int


class IngredientCreate(BaseModel):
    """Validation scheme to create ingredient"""
    title: str = "Название ингредиента"


class IngredientResponse(BaseModel):
    """Validation scheme to response ingredient"""
    id: int
    title: str


class SweetIngredientCreate(BaseModel):
    """Validation scheme to add ingredient to sweet"""
    sweet_id: int
    ingredient_id: int


class SweetIngredientResponse(BaseModel):
    """Validation scheme to response to ingredient of sweet"""
    sweet_id: int
    ingredient_id: int

from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class SweetCategory(SQLModel, table=True):
    """ SweetCategory Model for many-to-many link"""
    sweet_id: Optional[int] = Field(
        default=None, foreign_key="sweet.id", primary_key=True
    )
    category_id: Optional[int] = Field(
        default=None, foreign_key="category.id", primary_key=True
    )


class SweetIngredient(SQLModel, table=True):
    """ SweetIngredient Model for many-to-many link"""
    sweet_id: Optional[int] = Field(
        default=None, foreign_key="sweet.id", primary_key=True
    )
    ingredient_id: Optional[int] = Field(
        default=None, foreign_key="ingredient.id", primary_key=True
    )


class Category(SQLModel, table=True):
    """ Category Model """
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)

    sweets: List["Sweet"] = Relationship(back_populates="categories", link_model=SweetCategory)


class Ingredient(SQLModel, table=True):
    """ Ingredient Model """
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)

    sweets: List["Sweet"] = Relationship(back_populates="ingredients", link_model=SweetIngredient)


class Sweet(SQLModel, table=True):
    """ Sweet Model """
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str = Field()
    price: int = Field(index=True)
    in_stock: bool = Field(default=True)
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    edited_at: datetime = Field(default=datetime.utcnow(), nullable=False)

    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    categories: List[Category] = Relationship(back_populates="sweets",
                                              link_model=SweetCategory)
    ingredients: List[Ingredient] = Relationship(back_populates="sweets",
                                                 link_model=SweetIngredient)

    class Config:
        orm_mode = True



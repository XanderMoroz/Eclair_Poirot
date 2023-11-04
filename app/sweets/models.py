from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from sqlmodel import SQLModel, Field


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

    class Config:
        orm_mode = True

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

import uuid
from datetime import datetime
from typing import Optional
from pydantic import UUID4, validator
from sqlmodel import SQLModel, Field


class TokenBase(SQLModel):
    """ Return response data """
    user_id: int = Field(default=None)
    token: UUID4 = Field(default_factory=uuid.uuid4, alias="access_token")
    expires: datetime
    token_type: Optional[str] = "bearer"


class Token(TokenBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    class Config:
        orm_mode = True

    @validator("token")
    def hexlify_token(cls, value):
        """ Convert UUID to pure hex string """
        return value.hex


class UserBase(SQLModel):
    """ Return response data """
    id: int
    email: str
    name: str

    class Config:
        orm_mode = True


class UserCreate(SQLModel):
    """ Validate request data """
    email: str = "root@root.com"
    name: str = "JohnDoe"
    password: str = "123"


class User(SQLModel, table=True):
    """ Return detailed response data with token """
    id: int = Field(default=None, primary_key=True)
    email: str
    name: str
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True)

    class Config:
        orm_mode = True
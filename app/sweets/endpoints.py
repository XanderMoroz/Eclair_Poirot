from typing import Optional
from urllib.request import Request

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.db_config import get_session
from app.users.models import User
from app.sweets.schemas import SweetCreate, SweetResponse, CategoryCreate, CategoryResponse, SweetCategoryResponse
from app.sweets import db_manager
from app.core.dependencies import get_current_user
from sqlmodel import Session

user_sweets = APIRouter()
sweets = APIRouter()
admin_only = APIRouter()


@user_sweets.post("/sweets", response_model=SweetResponse, status_code=201)
def create_my_sweet(sweet_schema: SweetCreate,
                    session: Session = Depends(get_session),
                    current_user: User = Depends(get_current_user)):
    """
    **Creates a new sweet**

    Args:
     - sweet_schema (SweetCreate): Sweet creation data.
     - current_user (User): Current authenticated user.

    Returns: Newly created sweet object.
    """
    new_sweet = db_manager.create_sweet(sweet_schema, session, current_user)
    return new_sweet


@user_sweets.put("/sweets/{sweet_id}", response_model=SweetResponse)
def update_my_sweet(sweet_id: int,
                    sweet_data: SweetCreate,
                    session: Session = Depends(get_session),
                    current_user=Depends(get_current_user)):
    """
    **Updates a sweet by ID**

    Args:
     - sweet_id (int): ID of the sweet.
     - sweet_data (SweetCreate): Data for update sweet .
     - current_user (User): Current authenticated user.

    Returns: Updated sweet object.
    """
    sweet = db_manager.get_sweet_by_id(sweet_id, session)
    if sweet.user_id != current_user[0].id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to modify this sweet",
        )

    sweet = db_manager.update_sweet(
        sweet_id=sweet_id,
        payload=sweet_data,
        session=session)

    return sweet


@user_sweets.delete("/sweets/{sweet_id}", response_model=SweetResponse)
def delete_my_sweet(sweet_id: int,
                    session: Session = Depends(get_session),
                    current_user=Depends(get_current_user)):
    """
    **Deletes a sweet by ID**

    Args:
     - sweet_id (int): ID of the sweet.
     - current_user (User): Current authenticated user.

    Returns: Deleted sweet object.
    """
    sweet = db_manager.get_sweet_by_id(sweet_id, session)
    if sweet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sweet {sweet_id} not exist",
        )

    if sweet.user_id != current_user[0].id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to delete this sweet",
        )

    sweet = db_manager.delete_sweet(sweet_id, session)

    return sweet


@user_sweets.post("/sweet_category", response_model=SweetCategoryResponse, status_code=201)
def add_sweet_to_category(sweet_id: int, category_id: int,
                          session: Session = Depends(get_session),
                          current_user: User = Depends(get_current_user)):
    """
    *Adds a sweet to a category*

    Args:
     - sweet_id (int): ID of the sweet.
     - category_id (int): ID of the category.
     - session (Session): SQLAlchemy database session.
     - current_user (User): Current authenticated user.

    Returns: Newly created SweetCategory object.
    """
    sweet = db_manager.get_sweet_by_id(sweet_id, session)
    if sweet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sweet {sweet_id} not exist",
        )
    if sweet.user_id != current_user[0].id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to manage this sweet",
        )

    category = db_manager.get_category_by_id(category_id, session)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category {category_id} not exist",
        )

    new_sweet_category = db_manager.add_category_of_sweet(sweet_id, category_id, session)
    return new_sweet_category


@user_sweets.delete("/sweet_category", response_model=SweetCategoryResponse, status_code=201)
def remove_sweet_from_category(sweet_id: int, category_id: int,
                               session: Session = Depends(get_session),
                               current_user: User = Depends(get_current_user)):
    """
    **Removes a sweet from a category**

    Args:
     - sweet_id (int): ID of the sweet.
     - category_id (int): ID of the category.
     - session (Session): SQLAlchemy database session.
     - current_user (User): Current authenticated user.

    Returns: Removed SweetCategory object.
    """
    sweet = db_manager.get_sweet_by_id(sweet_id, session)
    if sweet.user_id != current_user[0].id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to manage this sweet",
        )

    category = db_manager.get_category_by_id(category_id, session)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category {category_id} not exist",
        )

    deleted_sweet_category = db_manager.remove_category_of_sweet(sweet_id, category_id, session)
    return deleted_sweet_category



@sweets.get("/sweets")
def get_sweets(page: int = 1, session: Session = Depends(get_session)):
    """
    **Retrieves a list of sweets with pagination**

    Args:
     - page (int): Page number.

    Returns: Dictionary containing total count and list of SweetResponse objects.
    """
    total_count = db_manager.get_deserts_count(session)
    deserts = db_manager.get_deserts(page, session)
    return {"total_count": total_count, "results": deserts}


@sweets.get("/sweets/{sweet_id}", response_model=SweetResponse)
def get_sweet(sweet_id: int, session: Session = Depends(get_session)):
    """
    **Retrieves a sweet by ID**

    Args:
     - sweet_id (int): ID of the sweet.

    Returns: Sweet object.
    """
    sweet = db_manager.get_sweet_by_id(sweet_id, session)

    if sweet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sweet {sweet_id} not exist",
        )

    return sweet


@sweets.get("/search")
def search_sweets(query: Optional[str] = None,
                  session: Session = Depends(get_session),):
    """
    **Searches for sweets based on a search query**

    Args:
     - query (str, optional): Search query string. Defaults to None.

    Returns: List of Sweet objects matching the search query.
    """
    search_result = db_manager.search_sweets(query, session=session)
    return search_result


@sweets.get("/filter")
def filter_sweets(min_price: Optional[int] = 0,
                  max_price: Optional[int] = 0,
                  session: Session = Depends(get_session)):
    """
    **Filters sweets based on price range**

    Args:
     - min_price (int, optional): Minimum price value. Defaults to 0.
     - max_price (int, optional): Maximum price value. Defaults to 0.

    Returns: List of Sweet objects within the specified price range.
    """
    filter_result = db_manager.filter_sweets(min_price, max_price, session=session)
    return filter_result


@admin_only.post("/categories", response_model=CategoryResponse, status_code=201)
def create_category(category_schema: CategoryCreate,
                    session: Session = Depends(get_session),):

    new_category = db_manager.create_category(category_schema, session)
    return new_category

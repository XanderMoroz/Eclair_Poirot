from fastapi import APIRouter, Depends, HTTPException, status

from app.core.db_config import get_session
from app.users.models import User
from app.sweets.models import SweetCreate, SweetResponse
from app.sweets import db_manager
from app.core.dependencies import get_current_user
from sqlmodel import Session

user_sweets = APIRouter()
sweets = APIRouter()


@user_sweets.post("/sweets", response_model=SweetResponse, status_code=201)
def create_my_sweet(sweet_schema: SweetCreate,
                    session: Session = Depends(get_session),
                    current_user: User = Depends(get_current_user)):
    """
    **Creates a new sweet**

    Args:
     - sweet_schema (SweetCreate): Sweet creation data.
     - session (Session): SQLAlchemy database session.
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
     - sweet_data (SweetCreate): Updated sweet data.
     - session (Session): SQLAlchemy database session.
     - current_user (User): Current authenticated user.

    Returns: Updated sweet object.
    """
    sweet = db_manager.get_sweet_by_id(sweet_id, session)
    if sweet.user_id != current_user[0].id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to modify this desert",
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
     - session (Session): SQLAlchemy database session.
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
            detail="You don't have access to delete this desert",
        )

    sweet = db_manager.delete_sweet(sweet_id, session)

    return sweet


@sweets.get("/sweets")
def get_sweets(page: int = 1, session: Session = Depends(get_session)):
    """
    **Retrieves a list of sweets with pagination**

    Args:
     - page (int): Page number.
     - session (Session): SQLAlchemy database session.

    Returns: Dictionary containing total count and list of SweetResponse objects.
    """
    total_count = db_manager.get_deserts_count(session)
    deserts = db_manager.get_deserts(page, session)
    return {"total_count": total_count, "results": deserts}


@sweets.get("/sweets/{sweet_id}", response_model=SweetResponse)
def get_sweet(sweet_id: int, session: Session = Depends(get_session)):
    """
    Retrieves a sweet by ID.

    Args:
     - sweet_id (int): ID of the sweet.
     - session (Session): SQLAlchemy database session.

    Returns: Sweet object.
    """
    sweet = db_manager.get_sweet_by_id(sweet_id, session)

    if sweet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sweet {sweet_id} not exist",
        )

    return sweet

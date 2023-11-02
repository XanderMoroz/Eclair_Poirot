from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.core.db_config import get_session
from app.core.dependencies import get_current_user
from app.users import models, security as security_utils, db_manager
from app.users.models import User, UserBase, UserCreate

auth_router = APIRouter()

@auth_router.post("/sign_up")
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    """
    **Sign-up a user with email and password.**

    Returns: Dictionary containing user and token properties.

    Raises: HTTPException: If the email already registered.
    """
    db_user = db_manager.get_user_by_email(user.email, session)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = db_manager.create_user(user, session)
    return new_user

@auth_router.post("/auth", response_model=models.TokenBase)
def authenticate_user(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    """
    **Authenticates a user with email and password.**

    Returns: Dictionary containing access token, expiration time, and token type.

    Raises: HTTPException: If the email or password is incorrect.
    """
    user = db_manager.get_user_by_email(email=form_data.username, session=session)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not security_utils.validate_password(password=form_data.password, hashed_password=user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = db_manager.create_user_token(user_id=user.id, session=session)
    uuid_to_str = str(token.token)
    token_dict = {"access_token": uuid_to_str, "expires": token.expires, "token_type": token.token_type}
    return token_dict


@auth_router.get("/users/me")
async def get_current_user(current_user: models.User = Depends(get_current_user)):
    """
    **Retrieves the current user.**

    Returns: Current user object.
    """
    return current_user


@auth_router.get("/users/{user_id}")
def get_user(user_id: int, session: Session = Depends(get_session)):
    """
    **Retrieves a user by ID.**

    Returns: User object.

    Raises: HTTPException: If the user does not exist.
    """
    user = db_manager.get_user_by_id(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} does not exist")
    return user


@auth_router.get("/users", response_model=list[UserBase])
def get_users(session: Session = Depends(get_session)):
    """
    **Retrieves a list of users.**

    Returns: List of User objects or empty list.
    """
    result = session.execute(select(User))
    users = result.scalars().all()
    return [UserBase(id=user.id, name=user.name, email=user.email) for user in users]

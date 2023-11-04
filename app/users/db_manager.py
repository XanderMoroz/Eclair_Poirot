from datetime import datetime, timedelta

from sqlalchemy import select
from sqlmodel import Session

from app.users.models import UserCreate, User, Token
from app.users.security import get_random_string, hash_password


def create_user(user: UserCreate, session: Session):
    """
    Creates a new user.

    Returns: Dictionary containing the user details and token information.
    """
    salt = get_random_string()
    hashed_password = hash_password(user.password, salt)
    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=f"{salt}${hashed_password}",
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    token = create_user_token(new_user.id, session)

    token_dict = {
        "token": token.token,
        "expires": token.expires
    }
    user_dict = {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email,
        "hashed_password": new_user.hashed_password,
        "is_active": True,
        "token": token_dict
    }

    return user_dict


def create_user_token(user_id: int, session: Session):
    """
    Creates a new token for a user.

    Returns: Token object.
    """
    new_user_token = Token(
        user_id=user_id,
        expires=datetime.now() + timedelta(weeks=2)
    )
    session.add(new_user_token)
    session.commit()
    session.refresh(new_user_token)

    return new_user_token


def get_user_by_token(token: str, session: Session):
    """
    Retrieves a user by token.

    Returns: User object or None if not found.
    """
    query = select(Token).where(Token.token == token).where(Token.expires > datetime.now())
    results = session.exec(query)
    t_token = results.one_or_none()
    token = t_token[0]

    query = select(User).where(User.id == token.user_id)
    results = session.exec(query)
    user = results.one_or_none()

    return user


def get_user_by_id(user_id: int, session: Session):
    """
    Retrieves a user by ID.

    Returns: User object or None if not found.
    """
    query = select(User).where(User.id == user_id)
    result = session.exec(query)
    scalar_obj = result.one_or_none()
    return scalar_obj


def get_user_by_email(email: str, session: Session):
    """
    Retrieves a user by email.

    Returns: User object or None if not found.
    """
    query = select(User).where(User.email == email)
    result = session.exec(query)
    user = result.one_or_none()
    return user

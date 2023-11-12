from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy import select, func
from sqlalchemy.orm import Session
# from sqlmodel import Session
from starlette.requests import Request

from app.core.app_config import settings
from app.core.db_config import get_session, admin_session
from app.users import db_manager
from app.users.models import User, Token
from app.users.security import validate_password


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]

        with admin_session(expire_on_commit=True) as session:
            stmt = select(User).where(User.email == email)
            result = session.execute(stmt)
            user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=400, detail="Incorrect email or password")

        if not validate_password(
                password=password, hashed_password=user.hashed_password
        ):
            raise HTTPException(status_code=400, detail="Incorrect email or password")

        print(user)

        with admin_session(expire_on_commit=True) as session:
            user_token = Token(user_id=user.id,
                               expires=datetime.now() + timedelta(weeks=2))

            session.add(user_token)
            session.commit()

        with admin_session(expire_on_commit=True) as session:
            stmt = select(Token).where(Token.user_id == user.id)
            result = session.execute(stmt)
            user_token = result.scalars()
            res = user_token.first()

        uuid_to_str = str(res.token)

        request.session.update({"token": uuid_to_str,
                                "user_id": res.user_id})

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        # Check the token in depth
        return True


authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)

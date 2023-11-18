from sqladmin import ModelView

from app.users.models import User, Token
from app.users.security import get_random_string, hash_password


class UserAdmin(ModelView, model=User):
    column_list = [User.id,
                   User.name,
                   User.email,
                   User.hashed_password]

    async def insert_model(self, request, data):
        salt = get_random_string()
        hashed_password = hash_password(data["hashed_password"], salt)
        data["hashed_password"] = f"{salt}${hashed_password}"
        return await super().insert_model(request, data)


class TokenAdmin(ModelView, model=Token):
    column_list = [Token.token,
                   Token.user_id,
                   Token.token_type,
                   Token.expires]

from sqladmin import ModelView

from app.users.models import User, Token


class UserAdmin(ModelView, model=User):
    column_list = [User.id,
                   User.name,
                   User.email,
                   User.hashed_password]


class TokenAdmin(ModelView, model=Token):
    column_list = [Token.token,
                   Token.user_id,
                   Token.token_type,
                   Token.expires]

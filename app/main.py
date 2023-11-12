
import uvicorn
from fastapi import FastAPI
from sqladmin import Admin
from app.core.admin_auth import authentication_backend, AdminAuth
from app.core.app_config import settings
from app.core.db_config import init_db, engine

from app.users import admin as users_admin
from app.users.endpoints import auth_router

from app.sweets import admin as sweets_admin
from app.sweets.endpoints import user_sweets, sweets, admin_only

# Main app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    openapi_url="/openapi.json",
    docs_url="/",
)

# Admin panel (SQLAdmin)
admin = Admin(app, engine, authentication_backend=authentication_backend)

# Admin views
admin.add_view(users_admin.UserAdmin)
admin.add_view(users_admin.TokenAdmin)
admin.add_view(sweets_admin.SweetAdmin)
admin.add_view(sweets_admin.CategoryAdmin)
admin.add_view(sweets_admin.SweetCategoryAdmin)
admin.add_view(sweets_admin.IngredientAdmin)
admin.add_view(sweets_admin.SweetIngredientAdmin)

# Routers
app.include_router(auth_router, prefix="", tags=["Authentication"])
app.include_router(user_sweets, prefix="/profile", tags=["Profile"])
app.include_router(sweets, prefix="", tags=["Sweets"])
app.include_router(admin_only, prefix="", tags=["Admin Only"])


@app.on_event("startup")
def on_startup():
    init_db()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
import uvicorn
from fastapi import FastAPI

from app.core.app_config import settings
from app.core.db_config import init_db

from app.users.endpoints import auth_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    openapi_url="/openapi.json",
    docs_url="/",
)

app.include_router(auth_router, prefix="", tags=["Authentication"])

@app.on_event("startup")
def on_startup():
    init_db()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
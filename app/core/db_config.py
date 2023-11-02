from app.core.app_config import settings
from sqlmodel import create_engine, SQLModel, Session

DB_USER = settings.DEFAULT_DB_USER
DB_PASS = settings.DEFAULT_DB_PASS
DB_HOST = settings.DEFAULT_DB_HOST
DB_PORT = settings.DEFAULT_DB_PORT
DB_NAME = settings.DEFAULT_DB_NAME

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
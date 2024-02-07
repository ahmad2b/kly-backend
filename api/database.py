from sqlmodel import SQLModel, create_engine, Session
from api.config import settings


# connect_args = {"check_same_thread": False}
engine = create_engine(settings.DATABASE_URI, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

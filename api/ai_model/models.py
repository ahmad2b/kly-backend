from sqlmodel import Field, SQLModel, create_engine, Session, select


class UrlRequest(SQLModel):
    original_url: str
    description: str | None = None

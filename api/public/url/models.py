from typing import Optional
from pydantic import HttpUrl
from typing import Annotated
from sqlmodel import Field, SQLModel
from datetime import datetime, timedelta


class URL(SQLModel, table=True):
    """
    URL model represents a URL record in the database.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[str] = Field(default=None, index=True)  # Change this line
    url: str = Field(default=None, nullable=False)
    short_url: str = Field(default=None, nullable=False, index=True, unique=True)
    clicks: Optional[int] = Field(default=0)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=None)
    expires_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.utcnow() + timedelta(days=30)
    )
    deleted_at: Optional[datetime] = Field(default_factory=None)


class UrlRequest(SQLModel):
    """
    UrlRequest model represents a request to create a new URL record.
    """

    url: HttpUrl = Field(...)
    short_url: Annotated[str, Field(..., max_length=2048)]
    user_id: Annotated[Optional[str], Field(default=None)]

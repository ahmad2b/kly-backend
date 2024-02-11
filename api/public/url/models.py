from typing import Optional
from datetime import datetime, timedelta
from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING


class URL(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[str] = Field(default=None, index=True)  # Change this line

    url: str = Field(nullable=False)
    short_url: str = Field(nullable=False, index=True, unique=True)

    clicks: Optional[int] = Field(default=0)

    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=None)
    expires_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.utcnow() + timedelta(days=30)
    )
    deleted_at: Optional[datetime] = Field(default_factory=None)


class URLCreate(SQLModel):
    url: str
    description: Optional[str] = None
    user_id: Optional[str] = None

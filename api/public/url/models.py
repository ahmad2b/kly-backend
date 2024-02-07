from typing import Optional
from datetime import datetime, timedelta
from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from api.public.user.models import User


class URL(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str = Field(nullable=False, index=True)
    short_url: str = Field(nullable=False, index=True, unique=True)
    clicks: Optional[int] = Field(default=0)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=None)
    expires_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.utcnow() + timedelta(days=30)
    )
    deleted_at: Optional[datetime] = Field(default_factory=None)

    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="urls")


class URLCreate(SQLModel):
    url: str
    user_id: Optional[int] = None
    expires_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.utcnow() + timedelta(days=30)
    )

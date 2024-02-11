"""drop exisitng table and create new url table

Revision ID: 81deef9c2bc1
Revises: 311976dfb5d7
Create Date: 2024-02-11 16:19:50.700311

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text


# revision identifiers, used by Alembic.
revision: str = "81deef9c2bc1"
down_revision: Union[str, None] = "311976dfb5d7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop the 'user' and 'url' tables
    op.execute(text('DROP TABLE IF EXISTS "user" CASCADE'))
    op.execute(text("DROP TABLE IF EXISTS url CASCADE"))

    # Create the new 'url' table
    op.create_table(
        "url",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, index=True),
        sa.Column("url", sa.String, nullable=False),
        sa.Column("short_url", sa.String, nullable=False, unique=True),
        sa.Column("clicks", sa.Integer, default=0),
        sa.Column("created_at", sa.DateTime, default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime),
        sa.Column(
            "expires_at",
            sa.DateTime,
            default=sa.text("(CURRENT_TIMESTAMP + INTERVAL '30 day')"),
        ),
        sa.Column("deleted_at", sa.DateTime),
    )


def downgrade() -> None:
    # Drop the new 'url' table
    op.execute(text("DROP TABLE IF EXISTS url CASCADE"))

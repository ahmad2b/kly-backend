"""drop hash_password from User

Revision ID: 5264addfa836
Revises: 607751276d64
Create Date: 2024-01-31 21:16:31.864903

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5264addfa836"
down_revision: Union[str, None] = "607751276d64"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_column("user", "hash_password")


def downgrade():
    op.add_column("user", sa.Column("hash_password", sa.String(), nullable=False))

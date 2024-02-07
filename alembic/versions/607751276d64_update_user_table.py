"""update User table

Revision ID: 607751276d64
Revises: 6cef3610b0e2
Create Date: 2024-01-31 20:16:46.226831

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import ForeignKeyConstraint

# revision identifiers, used by Alembic.
revision: str = "607751276d64"
down_revision: Union[str, None] = "6cef3610b0e2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("url") as batch_op:
        batch_op.drop_constraint("url_user_id_fkey", type_="foreignkey")
        batch_op.alter_column("user_id", existing_type=sa.Integer(), type_=sa.String())

    with op.batch_alter_table("user") as batch_op:
        batch_op.alter_column("id", existing_type=sa.Integer(), type_=sa.String())

    with op.batch_alter_table("url") as batch_op:
        batch_op.create_foreign_key("url_user_id_fkey", "user", ["user_id"], ["id"])


def downgrade() -> None:
    with op.batch_alter_table("url") as batch_op:
        batch_op.drop_constraint("url_user_id_fkey", type_="foreignkey")
        batch_op.alter_column("user_id", existing_type=sa.String(), type_=sa.Integer())

    with op.batch_alter_table("user") as batch_op:
        batch_op.alter_column("id", existing_type=sa.String(), type_=sa.Integer())

    with op.batch_alter_table("url") as batch_op:
        batch_op.create_foreign_key("url_user_id_fkey", "user", ["user_id"], ["id"])

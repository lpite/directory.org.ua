"""Make en non nullable

Revision ID: d58a3bf35637
Revises: 35fbe8b0b2b5
Create Date: 2022-02-05 20:44:42.564017

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d58a3bf35637"
down_revision = "35fbe8b0b2b5"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("katottg", "name_en", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("koatuu", "name_en", existing_type=sa.VARCHAR(), nullable=False)


def downgrade():
    op.alter_column("koatuu", "name_en", existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column("katottg", "name_en", existing_type=sa.VARCHAR(), nullable=True)

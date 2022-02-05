"""Add name_en columns

Revision ID: 35fbe8b0b2b5
Revises: 8512fa6a4a52
Create Date: 2022-02-05 20:28:42.291762

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "35fbe8b0b2b5"
down_revision = "8512fa6a4a52"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("katottg", sa.Column("name_en", sa.String(), nullable=True))
    op.add_column("koatuu", sa.Column("name_en", sa.String(), nullable=True))


def downgrade():
    op.drop_column("koatuu", "name_en")
    op.drop_column("katottg", "name_en")

"""Add table tokens

Revision ID: eeeede4c6639
Revises: d58a3bf35637
Create Date: 2022-02-05 21:35:46.857812

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "eeeede4c6639"
down_revision = "d58a3bf35637"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "tokens",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column("token", sa.String(), nullable=True),
        sa.Column("comment", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_tokens_token"), "tokens", ["token"], unique=True)


def downgrade():
    op.drop_index(op.f("ix_tokens_token"), table_name="tokens")
    op.drop_table("tokens")

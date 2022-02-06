"""Rename token to secret in table tokens

Revision ID: 52e47585603b
Revises: eeeede4c6639
Create Date: 2022-02-06 13:18:34.464344

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "52e47585603b"
down_revision = "eeeede4c6639"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("tokens", sa.Column("secret", sa.String(), nullable=True))
    op.drop_index("ix_tokens_token", table_name="tokens")
    op.create_index(op.f("ix_tokens_secret"), "tokens", ["secret"], unique=True)
    op.drop_column("tokens", "token")


def downgrade():
    op.add_column(
        "tokens", sa.Column("token", sa.VARCHAR(), autoincrement=False, nullable=True)
    )
    op.drop_index(op.f("ix_tokens_secret"), table_name="tokens")
    op.create_index("ix_tokens_token", "tokens", ["token"], unique=False)
    op.drop_column("tokens", "secret")

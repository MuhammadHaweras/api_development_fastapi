"""create a users table

Revision ID: 6f68b61ee4fa
Revises: 4098505024a9
Create Date: 2025-07-26 16:36:52.398317

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6f68b61ee4fa'
down_revision: Union[str, Sequence[str], None] = '4098505024a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('user',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(length=255), nullable=False),
                    sa.Column('password', sa.String(length=255), nullable=False),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email', name='uq_user_email')
                    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('user')
    pass

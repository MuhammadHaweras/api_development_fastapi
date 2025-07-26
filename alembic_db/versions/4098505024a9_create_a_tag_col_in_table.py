"""create a tag col in  table

Revision ID: 4098505024a9
Revises: 8b13d0938d6f
Create Date: 2025-07-26 16:30:13.003017

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4098505024a9'
down_revision: Union[str, Sequence[str], None] = '8b13d0938d6f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('post',
                  sa.Column('tag', sa.String(length=255), nullable=True))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('post', 'tag')
    pass

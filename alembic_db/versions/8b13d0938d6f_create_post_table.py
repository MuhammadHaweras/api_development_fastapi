"""create post table

Revision ID: 8b13d0938d6f
Revises: 
Create Date: 2025-07-26 16:19:13.470715

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b13d0938d6f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('post',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(length=255), nullable=False),
                    sa.Column('content', sa.Text(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
                    # sa.Column('user_id', sa.Integer(), nullable=False),
                    # sa.Column('published', sa.Boolean(), server_default='TRUE', nullable=False),
                    # sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id'),
                    # sa.UniqueConstraint('title', name='uq_post_title')
                    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('post')
    pass

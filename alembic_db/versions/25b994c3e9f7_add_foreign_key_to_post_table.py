"""add foreign key to post table

Revision ID: 25b994c3e9f7
Revises: 6f68b61ee4fa
Create Date: 2025-07-26 16:42:19.225820

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '25b994c3e9f7'
down_revision: Union[str, Sequence[str], None] = '6f68b61ee4fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('post',
                  sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(
        'fk_post_user',
        source_table='post',
        referent_table='user',
        local_cols=['user_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('fk_post_user', 'post', type_='foreignkey')
    op.drop_column('post', 'user_id')
    pass

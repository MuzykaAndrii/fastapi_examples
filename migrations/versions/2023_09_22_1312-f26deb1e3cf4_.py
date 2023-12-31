"""empty message

Revision ID: f26deb1e3cf4
Revises: 287e66bdd558
Create Date: 2023-09-22 13:12:54.866736

"""
from typing import (
    Sequence,
    Union,
)

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'f26deb1e3cf4'
down_revision: Union[str, None] = '287e66bdd558'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('roles', 'perms')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('roles', sa.Column('perms', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###

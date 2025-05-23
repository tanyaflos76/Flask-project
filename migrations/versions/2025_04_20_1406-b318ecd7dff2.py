"""Add image name column

Revision ID: b318ecd7dff2
Revises: 7601fcfd91ec
Create Date: 2025-04-20 14:06:38.975144+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "b318ecd7dff2"
down_revision: Union[str, None] = "7601fcfd91ec"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("wishes", sa.Column("image_name", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("wishes", "image_name")

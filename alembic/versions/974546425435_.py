"""empty message

Revision ID: 974546425435
Revises: 895d97556701
Create Date: 2024-11-15 17:27:07.377475

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "974546425435"
down_revision: Union[str, None] = "895d97556701"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("products", sa.Column("name", sa.String(), nullable=True))
    op.create_index(op.f("ix_products_name"), "products", ["name"], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_products_name"), table_name="products")
    op.drop_column("products", "name")
    # ### end Alembic commands ###

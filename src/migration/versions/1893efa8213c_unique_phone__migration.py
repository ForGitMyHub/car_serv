"""unique_phone__migration

Revision ID: 1893efa8213c
Revises: d25e10d414f9
Create Date: 2023-05-13 00:32:49.019145

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1893efa8213c'
down_revision = 'd25e10d414f9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'clients', ['phone'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'clients', type_='unique')
    # ### end Alembic commands ###

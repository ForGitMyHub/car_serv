"""two_migration

Revision ID: c3ad78d426a7
Revises: 312aa76f2779
Create Date: 2023-05-02 23:28:46.804305

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c3ad78d426a7'
down_revision = '312aa76f2779'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cars', sa.Column('photo_link', postgresql.JSONB(astext_type=sa.Text()), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cars', 'photo_link')
    # ### end Alembic commands ###

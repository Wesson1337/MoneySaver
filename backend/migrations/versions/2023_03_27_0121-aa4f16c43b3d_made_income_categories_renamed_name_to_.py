"""made income categories, renamed "name" to "comment" in spending and income

Revision ID: aa4f16c43b3d
Revises: 044829375f58
Create Date: 2023-03-27 01:21:33.698569

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa4f16c43b3d'
down_revision = '044829375f58'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('income', sa.Column('category', sa.String(length=255), nullable=False))
    op.add_column('income', sa.Column('comment', sa.String(length=255), nullable=True))
    op.drop_column('income', 'name')
    op.add_column('spending', sa.Column('comment', sa.String(length=255), nullable=True))
    op.drop_column('spending', 'name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('spending', sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    op.drop_column('spending', 'comment')
    op.add_column('income', sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    op.drop_column('income', 'comment')
    op.drop_column('income', 'category')
    # ### end Alembic commands ###

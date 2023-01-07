"""removed goal and spending category models

Revision ID: 4c0b54fcac7f
Revises: cfbaa681d6ba
Create Date: 2023-01-06 03:17:00.101600

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '4c0b54fcac7f'
down_revision = 'cfbaa681d6ba'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('spending_goal_id_fkey', 'spending', type_='foreignkey')
    op.drop_constraint('spending_category_id_fkey', 'spending', type_='foreignkey')
    op.drop_table('goal')
    op.drop_table('spending_category')
    op.drop_column('spending', 'goal_id')
    op.drop_column('spending', 'category_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('spending', sa.Column('category_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('spending', sa.Column('goal_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('spending_category_id_fkey', 'spending', 'spending_category', ['category_id'], ['id'])
    op.create_foreign_key('spending_goal_id_fkey', 'spending', 'goal', ['goal_id'], ['id'])
    op.create_table('spending_category',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='spending_category_pkey')
    )
    op.create_table('goal',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('target_amount', sa.NUMERIC(), autoincrement=False, nullable=False),
    sa.Column('balance', sa.NUMERIC(), autoincrement=False, nullable=False),
    sa.Column('currency', sa.VARCHAR(length=3), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='goal_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='goal_pkey')
    )
    # ### end Alembic commands ###

"""added user model

Revision ID: feb3428bd784
Revises: a2f3c9b5ba3d
Create Date: 2022-12-07 04:05:58.704878

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'feb3428bd784'
down_revision = 'a2f3c9b5ba3d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.add_column('account', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'account', 'user', ['user_id'], ['id'])
    op.add_column('goal', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'goal', 'user', ['user_id'], ['id'])
    op.add_column('income', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'income', 'user', ['user_id'], ['id'])
    op.add_column('spending', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'spending', 'user', ['user_id'], ['id'])
    op.add_column('spending_category', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'spending_category', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'spending_category', type_='foreignkey')
    op.drop_column('spending_category', 'user_id')
    op.drop_constraint(None, 'spending', type_='foreignkey')
    op.drop_column('spending', 'user_id')
    op.drop_constraint(None, 'income', type_='foreignkey')
    op.drop_column('income', 'user_id')
    op.drop_constraint(None, 'goal', type_='foreignkey')
    op.drop_column('goal', 'user_id')
    op.drop_constraint(None, 'account', type_='foreignkey')
    op.drop_column('account', 'user_id')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
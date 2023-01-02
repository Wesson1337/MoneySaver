import datetime
from decimal import Decimal

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from ..database import Base


class Income(Base):
    __tablename__ = 'income'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    name = sa.Column(sa.String(255), nullable=False)
    currency = sa.Column(sa.String(3), nullable=False)
    replenishment_account_id = sa.Column(sa.ForeignKey('account.id'), nullable=False)
    amount = sa.Column(sa.DECIMAL, nullable=False)
    amount_in_account_currency_at_creation = sa.Column(sa.DECIMAL, nullable=False)
    created_at = sa.Column(sa.DateTime, default=datetime.datetime.now(), nullable=False)
    user_id = sa.Column(sa.ForeignKey('user.id'), nullable=False)

    user = relationship('User', back_populates='incomes')
    replenishment_account = relationship('Account', back_populates='incomes')


class Account(Base):
    __tablename__ = 'account'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    name = sa.Column(sa.String(255), nullable=False)
    type = sa.Column(sa.String(12), nullable=False)
    balance = sa.Column(sa.DECIMAL, default=Decimal(0), nullable=False)
    currency = sa.Column(sa.String(3), nullable=False)
    is_active = sa.Column(sa.Boolean, default=True, nullable=False)
    user_id = sa.Column(sa.ForeignKey('user.id'), nullable=False)

    user = relationship('User', back_populates='accounts')
    incomes = relationship('Income', back_populates='replenishment_account')
    spendings = relationship('Spending', back_populates='receipt_account')


class Spending(Base):
    __tablename__ = 'spending'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    name = sa.Column(sa.String(255), nullable=False)
    category_id = sa.Column(sa.ForeignKey('spending_category.id'), nullable=False)
    receipt_account_id = sa.Column(sa.ForeignKey('account.id'), nullable=False)
    amount = sa.Column(sa.DECIMAL, nullable=False)
    amount_in_account_currency_at_creation = sa.Column(sa.DECIMAL, nullable=False)
    currency = sa.Column(sa.String(3), nullable=False)
    goal_id = sa.Column(sa.Integer, sa.ForeignKey('goal.id'))
    created_at = sa.Column(sa.DateTime, default=datetime.datetime.now(), nullable=False)
    user_id = sa.Column(sa.ForeignKey('user.id'), nullable=False)

    user = relationship('User', back_populates='spendings')
    receipt_account = relationship('Account', back_populates='spendings')
    category = relationship('SpendingCategory', back_populates='spendings')
    goal = relationship('Goal', back_populates='spendings')


class SpendingCategory(Base):
    __tablename__ = 'spending_category'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    name = sa.Column(sa.String(255), nullable=False)
    spending_limit = sa.Column(sa.DECIMAL)
    spent_in_month = sa.Column(sa.DECIMAL)
    user_id = sa.Column(sa.ForeignKey('user.id'), nullable=False)

    user = relationship('User', back_populates='spending_categories')
    spendings = relationship('Spending', back_populates='category')


class Goal(Base):
    __tablename__ = 'goal'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    name = sa.Column(sa.String(255), nullable=False)
    target_amount = sa.Column(sa.DECIMAL, nullable=False)
    balance = sa.Column(sa.DECIMAL, nullable=False)
    currency = sa.Column(sa.String(3), nullable=False)
    user_id = sa.Column(sa.ForeignKey('user.id'), nullable=False)

    user = relationship('User', back_populates='goals')
    spendings = relationship('Spending', back_populates='goal')

    async def get_the_rest_amount(self) -> Decimal:
        return Decimal(self.target_amount) - Decimal(self.balance)

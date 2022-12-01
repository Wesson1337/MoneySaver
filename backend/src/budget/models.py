import datetime
from decimal import Decimal

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from ..database import Base


class Income(Base):
    __tablename__ = 'income'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    name = sa.Column(sa.String(255))
    currency = sa.Column(sa.String(3))
    replenishment_account_id = sa.Column(sa.Integer, sa.ForeignKey('account.id'))
    amount = sa.Column(sa.DECIMAL())
    created_at = sa.Column(sa.DateTime, default=datetime.datetime.now())

    replenishment_account = relationship('Account', back_populates='incomes')


class Account(Base):
    __tablename__ = 'account'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    name = sa.Column(sa.String(255))
    type = sa.Column(sa.String(12))
    balance = sa.Column(sa.DECIMAL())
    currency = sa.Column(sa.String(3))

    incomes = relationship('Income', back_populates='replenishment_account')
    spendings = relationship('Spending', back_populates='receipt_account')


class Spending(Base):
    __tablename__ = 'spending'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    name = sa.Column(sa.String(255))
    category_id = sa.Column(sa.Integer, sa.ForeignKey('spending_category.id'))
    receipt_account_id = sa.Column(sa.Integer, sa.ForeignKey('account.id'))
    amount = sa.Column(sa.DECIMAL())
    currency = sa.Column(sa.String(3))
    goal_id = sa.Column(sa.Integer, sa.ForeignKey('goal.id'))
    created_at = sa.Column(sa.DateTime, default=datetime.datetime.now())

    receipt_account = relationship('Account', back_populates='spendings')
    category = relationship('SpendingCategory', back_populates='spendings')
    goal = relationship('Goal', back_populates='spendings')


class SpendingCategory(Base):
    __tablename__ = 'spending_category'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    name = sa.Column(sa.String(255))
    spending_limit = sa.Column(sa.DECIMAL())
    spent_in_month = sa.Column(sa.DECIMAL())

    spendings = relationship('Spending', back_populates='category')


class Goal(Base):
    __tablename__ = 'goal'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    name = sa.Column(sa.String(255))
    target_amount = sa.Column(sa.DECIMAL())
    balance = sa.Column(sa.DECIMAL())
    currency = sa.Column(sa.String(3))

    spendings = relationship('Spending', back_populates='goal')

    async def get_the_rest_amount(self) -> Decimal:
        return Decimal(self.target_amount) - Decimal(self.balance)

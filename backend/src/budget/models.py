import datetime
from decimal import Decimal

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from ..config import Currencies, AccountTypes
from ..database import Base


class Income(Base):
    __tablename__ = 'income'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    name = sa.Column(sa.String(255))
    currency = sa.Column(sa.Enum(Currencies))
    replenishment_account_id = sa.Column(sa.Integer, sa.ForeignKey('account.id'))
    amount = sa.Column(sa.DECIMAL())
    created_at = sa.Column(sa.DateTime, default=datetime.datetime.now())


class Account(Base):
    __tablename__ = 'account'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    name = sa.Column(sa.String(255))
    type = sa.Column(sa.Enum(AccountTypes))
    balance = sa.Column(sa.DECIMAL())
    currency = sa.Column(sa.Enum(Currencies))

    incomes = relationship('Income', backref='replenishment_account')
    spendings = relationship('Spending', backref='receipt_account')


class Spending(Base):
    __tablename__ = 'spending'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    name = sa.Column(sa.String(255))
    category_id = sa.Column(sa.Integer, sa.ForeignKey('spending_category.id'))
    receipt_account_id = sa.Column(sa.Integer, sa.ForeignKey('account.id'))
    amount = sa.Column(sa.DECIMAL())
    currency = sa.Column(sa.Enum(Currencies))
    goal_id = sa.Column(sa.Integer, sa.ForeignKey('goal.id'))
    created_at = sa.Column(sa.DateTime, default=datetime.datetime.now())


class SpendingCategory(Base):
    __tablename__ = 'spending_category'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    name = sa.Column(sa.String(255))
    spending_limit = sa.Column(sa.DECIMAL())
    limit_duration = sa.Column(sa.Integer)

    spendings = relationship('Spending', backref='category')


class Goal(Base):
    __tablename__ = 'goal'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    name = sa.Column(sa.String(255))
    target_amount = sa.Column(sa.DECIMAL())
    balance = sa.Column(sa.DECIMAL())
    currency = sa.Column(sa.Enum(Currencies))

    spendings = relationship('Spending', backref='goal')

    async def get_the_rest_amount(self) -> Decimal:
        return Decimal(self.target_amount) - Decimal(self.balance)

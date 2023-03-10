import datetime
from decimal import Decimal

import sqlalchemy as sa
from sqlalchemy import func
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
    created_at = sa.Column(sa.DateTime, server_default=func.now(), nullable=False)
    user_id = sa.Column(sa.ForeignKey('user.id'), nullable=False)

    user = relationship('User', back_populates='incomes')
    replenishment_account = relationship('Account', back_populates='incomes')

    __mapper_args__ = {"eager_defaults": True}


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
    receipt_account_id = sa.Column(sa.ForeignKey('account.id'), nullable=False)
    category = sa.Column(sa.String(255), nullable=False)
    amount = sa.Column(sa.DECIMAL, nullable=False)
    amount_in_account_currency_at_creation = sa.Column(sa.DECIMAL, nullable=False)
    currency = sa.Column(sa.String(3), nullable=False)
    created_at = sa.Column(sa.DateTime, server_default=func.now(), nullable=False)
    user_id = sa.Column(sa.ForeignKey('user.id'), nullable=False)

    user = relationship('User', back_populates='spendings')
    receipt_account = relationship('Account', back_populates='spendings')

    __mapper_args__ = {"eager_defaults": True}

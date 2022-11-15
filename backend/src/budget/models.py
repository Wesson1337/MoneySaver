import datetime

import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

from ..database import Base

CURRENCIES = [
    ('US', 'American dollar'),
    ('RU', 'Russian ruble'),
    ('CNY', 'Renminbi')
]


class Income(Base):
    __tablename__ = 'income'

    name = sa.Column(sa.String(255))
    currency = sa.Column(ChoiceType(CURRENCIES))
    replenishment_account_id = sa.Column(sa.Integer, sa.ForeignKey('account.id'))
    amount = sa.Column(sa.Float(asdecimal=True))
    created_at = sa.Column(sa.DateTime, default=datetime.datetime.now())


class Account(Base):
    TYPES = [
        ('BA', 'Bank account'),
        ('WA', 'Wallet')
    ]

    __tablename__ = 'account'

    name = sa.Column(sa.String(255))
    type = sa.Column(ChoiceType(TYPES))
    balance = sa.Column(sa.Float(asdecimal=True))

    incomes = relationship('Income', backref='account')
    spendings = relationship('Spending', backref='account')
    goal_spendings = relationship('GoalSpending', backref='account')


class Spending(Base):
    __tablename__ = 'spending'

    name = sa.Column(sa.String(255))
    category_id = sa.Column(sa.Integer, sa.ForeignKey('spending_category.id'))
    receipt_account_id = sa.Column(sa.Integer, sa.ForeignKey('account.id'))
    amount = sa.Column(sa.Float(asdecimal=True))
    created_at = sa.Column(sa.DateTime, default=datetime.datetime.now())


class SpendingCategory(Base):
    __tablename__ = 'spending_category'

    name = sa.Column(sa.String(255))
    spending_limit = sa.Column(sa.Float(asdecimal=True))
    limit_duration = sa.Column(sa.Integer)

    spendings = relationship('Spending', backref='category')


class GoalSpending(Base):
    __tablename__ = 'goal_spending'

    account_id = sa.Column(sa.Integer, sa.ForeignKey('account.id'))
    goal_id = sa.Column(sa.Integer, sa.ForeignKey('goal.id'))
    amount = sa.Column(sa.Float(asdecimal=True))
    created_at = sa.Column(sa.DateTime, default=datetime.datetime.now())


class Goal(Base):
    __tablename__ = 'goal'

    name = sa.Column(sa.String(255))
    target_amount = sa.Column(sa.Float(asdecimal=True))
    balance = sa.Column(sa.Float(asdecimal=True))

    goal_spendings = relationship('GoalSpending', backref='goal')

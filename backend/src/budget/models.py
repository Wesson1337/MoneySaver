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

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
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

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    name = sa.Column(sa.String(255))
    type = sa.Column(ChoiceType(TYPES))
    balance = sa.Column(sa.Float(asdecimal=True))
    currency = sa.Column(ChoiceType(CURRENCIES))

    incomes = relationship('Income', backref='account')
    spendings = relationship('Spending', backref='account')
    goal_spendings = relationship('GoalSpending', backref='account')


class Spending(Base):
    __tablename__ = 'spending'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    name = sa.Column(sa.String(255))
    category_id = sa.Column(sa.Integer, sa.ForeignKey('spending_category.id'))
    receipt_account_id = sa.Column(sa.Integer, sa.ForeignKey('account.id'))
    amount = sa.Column(sa.Float(asdecimal=True))
    currency = sa.Column(ChoiceType(CURRENCIES))
    created_at = sa.Column(sa.DateTime, default=datetime.datetime.now())


class SpendingCategory(Base):
    __tablename__ = 'spending_category'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    name = sa.Column(sa.String(255))
    spending_limit = sa.Column(sa.Float(asdecimal=True))
    limit_duration = sa.Column(sa.Integer)

    spendings = relationship('Spending', backref='category')


class GoalSpending(Base):
    __tablename__ = 'goal_spending'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    account_id = sa.Column(sa.Integer, sa.ForeignKey('account.id'))
    goal_id = sa.Column(sa.Integer, sa.ForeignKey('goal.id'))
    amount = sa.Column(sa.Float(asdecimal=True))
    currency = sa.Column(ChoiceType(CURRENCIES))
    created_at = sa.Column(sa.DateTime, default=datetime.datetime.now())


class Goal(Base):
    __tablename__ = 'goal'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    name = sa.Column(sa.String(255))
    target_amount = sa.Column(sa.Float(asdecimal=True))
    balance = sa.Column(sa.Float(asdecimal=True))
    currency = sa.Column(ChoiceType(CURRENCIES))

    goal_spendings = relationship('GoalSpending', backref='goal')

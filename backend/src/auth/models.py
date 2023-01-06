from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from backend.src.database import Base


class User(Base):
    __tablename__ = "user"

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    email = sa.Column(sa.String(255), unique=True, index=True, nullable=False)
    hashed_password = sa.Column(sa.String, nullable=False)
    is_active = sa.Column(sa.Boolean, default=True, nullable=False)
    is_superuser = sa.Column(sa.Boolean, default=False, nullable=False)
    created_at = sa.Column(sa.DateTime(), default=datetime.now(), nullable=False)

    incomes = relationship('Income', back_populates='user')
    accounts = relationship('Account', back_populates='user')
    spendings = relationship('Spending', back_populates='user')


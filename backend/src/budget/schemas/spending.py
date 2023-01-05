import datetime
from typing import Optional
from decimal import Decimal
from pydantic import constr, conint, condecimal

from backend.src.budget.schemas.account import AccountSchemaOut
from backend.src.budget.schemas.spending_category import SpendingCategorySchemaOut
from backend.src.config import Currencies
from backend.src.utils import BaseORMSchema


class SpendingSchemaIn(BaseORMSchema):
    name: constr(max_length=255)
    user_id: conint(ge=1)
    category_id: conint(ge=1)
    receipt_account_id: conint(ge=1)
    goal_id: Optional[conint(ge=1)] = None
    amount: condecimal(gt=Decimal(0), decimal_places=2)
    currency: Currencies


class SpendingSchemaOut(BaseORMSchema):
    id: conint(ge=1)
    name: constr(max_length=255)
    user_id: conint(ge=1)
    category: SpendingCategorySchemaOut
    receipt_account: AccountSchemaOut
    goal_id: Optional[conint(ge=1)]
    amount: condecimal(gt=Decimal(0))
    amount_in_account_currency_at_creation: condecimal(gt=Decimal(0))
    currency: Currencies
    created_at: datetime.datetime


class SpendingSchemaPatch(BaseORMSchema):
    name: Optional[constr(max_length=255)]
    amount: condecimal(gt=Decimal(0), decimal_places=2)

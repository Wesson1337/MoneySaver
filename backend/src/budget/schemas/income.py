import datetime
from decimal import Decimal
from typing import Optional

from pydantic import constr, condecimal, conint

from backend.src.budget.config import Currencies, IncomeCategories
from backend.src.budget.schemas.account import AccountSchemaOut
from backend.src.schema import BaseORMSchema


class IncomeSchemaIn(BaseORMSchema):
    user_id: conint(ge=1)
    currency: Currencies
    category: IncomeCategories
    replenishment_account_id: conint(ge=1)
    amount: condecimal(gt=Decimal(0), decimal_places=2, lt=Decimal(1000000000))
    comment: Optional[constr(max_length=255)]


class IncomeSchemaPatch(BaseORMSchema):
    amount: Optional[condecimal(gt=Decimal(0), decimal_places=2, lt=Decimal(1000000000))]
    category: Optional[IncomeCategories]
    comment: Optional[constr(max_length=255)]


class IncomeSchemaOut(BaseORMSchema):
    id: int
    user_id: int
    currency: Currencies
    category: IncomeCategories
    # from db we get float, so we need to check decimal_places in amount field only in Patch, In schemas
    amount: condecimal(gt=Decimal(0))
    amount_in_account_currency_at_creation: condecimal(gt=Decimal(0))
    replenishment_account: AccountSchemaOut
    created_at: datetime.datetime
    comment: Optional[constr(max_length=255)]

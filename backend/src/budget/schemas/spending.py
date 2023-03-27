import datetime
from decimal import Decimal
from typing import Optional

from pydantic import constr, conint, condecimal

from backend.src.budget.config import Currencies, SpendingCategories
from backend.src.budget.schemas.account import AccountSchemaOut
from backend.src.schema import BaseORMSchema


class SpendingSchemaIn(BaseORMSchema):
    user_id: conint(ge=1)
    category: SpendingCategories
    receipt_account_id: conint(ge=1)
    amount: condecimal(gt=Decimal(0), decimal_places=2, lt=Decimal(1000000000))
    currency: Currencies
    comment: Optional[constr(max_length=255)]


class SpendingSchemaOut(BaseORMSchema):
    id: conint(ge=1)
    user_id: conint(ge=1)
    category: SpendingCategories
    receipt_account: AccountSchemaOut
    amount: condecimal(gt=Decimal(0))
    amount_in_account_currency_at_creation: condecimal(gt=Decimal(0))
    currency: Currencies
    created_at: datetime.datetime
    comment: Optional[constr(max_length=255)]


class SpendingSchemaPatch(BaseORMSchema):
    amount: Optional[condecimal(gt=Decimal(0), decimal_places=2, lt=Decimal(1000000000))]
    category: Optional[SpendingCategories]
    comment: Optional[constr(max_length=255)]

from decimal import Decimal
from typing import Optional

from pydantic import constr, conint, condecimal

from backend.src.budget.config import Currencies, AccountTypes
from backend.src.schema import BaseORMSchema


class AccountSchemaIn(BaseORMSchema):
    name: constr(max_length=255)
    user_id: conint(ge=1)
    type: AccountTypes
    currency: Currencies
    balance: condecimal(ge=Decimal(0), decimal_places=2, lt=Decimal(1000000000))


class AccountSchemaOut(BaseORMSchema):
    id: conint(ge=1)
    name: constr(max_length=255)
    user_id: conint(ge=1)
    type: AccountTypes
    is_active: bool
    balance: condecimal(ge=0)
    currency: Currencies


class AccountSchemaPatch(BaseORMSchema):
    name: Optional[constr(max_length=255)]
    type: Optional[AccountTypes]
    is_active: Optional[bool]

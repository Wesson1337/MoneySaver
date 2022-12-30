from decimal import Decimal

from pydantic import BaseModel, constr

from backend.src.config import AccountTypes, Currencies
from backend.src.utils import BaseORMSchema


class AccountSchemaIn(BaseORMSchema):
    name: constr(max_length=255)
    type: AccountTypes
    balance: Decimal
    currency: Currencies


class AccountSchemaOut(BaseORMSchema):
    id: int
    name: constr(max_length=255)
    type: AccountTypes
    balance: Decimal
    currency: Currencies

from pydantic import constr, conint, condecimal

from backend.src.config import AccountTypes, Currencies
from backend.src.utils import BaseORMSchema


class AccountSchemaIn(BaseORMSchema):
    name: constr(max_length=255)
    user_id: conint(gt=0)
    type: AccountTypes
    currency: Currencies


class AccountSchemaOut(BaseORMSchema):
    id: int
    name: constr(max_length=255)
    type: AccountTypes
    is_active: bool
    balance: condecimal(ge=0)
    currency: Currencies


class AccountSchemaPatch(BaseORMSchema):
    name: constr(max_length=255)
    type: AccountTypes
    is_active: bool

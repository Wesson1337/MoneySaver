from decimal import Decimal

from pydantic import BaseModel, constr

from backend.src.config import AccountTypes, Currencies


class BaseAccountSchema(BaseModel):
    class Config:
        orm_mode = True


class AccountSchemaIn(BaseAccountSchema):
    name: constr(max_length=255)
    type: AccountTypes
    balance: Decimal
    currency: Currencies


class AccountSchemaOut(BaseAccountSchema):
    id: int
    name: constr(max_length=255)
    type: AccountTypes
    balance: Decimal
    currency: Currencies

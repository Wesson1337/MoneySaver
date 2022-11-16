from decimal import Decimal

from pydantic import BaseModel, constr, condecimal, conint

from backend.src.budget.schemas.account import AccountSchemaOut
from backend.src.config import Currencies


class BaseIncomeSchema(BaseModel):
    name: constr(max_length=255)
    currency: Currencies
    amount: condecimal(gt=Decimal(0))

    class Config:
        orm_mode = True


class IncomeSchemaIn(BaseIncomeSchema):
    replenishment_account_id: conint(ge=1)
    amount = condecimal(gt=Decimal(0), decimal_places=2)


class IncomeSchemaOut(BaseIncomeSchema):
    id: int
    replenishment_account: AccountSchemaOut




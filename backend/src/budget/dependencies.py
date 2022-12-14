import datetime
from dataclasses import dataclass
from typing import Optional

from fastapi import Query

from backend.src.budget.config import Currencies, SpendingCategories
from backend.src.dependencies import BaseQueryParams


@dataclass
class IncomeQueryParams(BaseQueryParams):
    currency: Optional[Currencies] = Query(default=None)
    created_at_ge: Optional[datetime.datetime] = Query(
        default=None,
        example="2022-11-19T11:49:27.702655",
        description="Filters incomes created after this datetime"
    )
    created_at_le: Optional[datetime.datetime] = Query(
        default=None,
        example="2022-11-20T00:00:00.000",
        description="Filters incomes created before this datetime"
    )


@dataclass
class AccountQueryParams(BaseQueryParams):
    currency: Optional[Currencies] = Query(default=None)
    is_active: Optional[bool] = Query(default=None)


@dataclass
class SpendingQueryParams(BaseQueryParams):
    currency: Optional[Currencies] = Query(default=None)
    created_at_ge: Optional[datetime.datetime] = Query(
        default=None,
        example="2022-11-19T11:49:27.702655",
        description="Filters spendings created after this datetime"
    )
    created_at_le: Optional[datetime.datetime] = Query(
        default=None,
        example="2022-11-20T00:00:00.000",
        description="Filters spendings created before this datetime"
    )
    category: Optional[SpendingCategories] = Query(default=None)



import datetime
from dataclasses import dataclass
from typing import Optional

from fastapi import Query

from backend.src.config import Currencies
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
    active: Optional[bool] = Query(default=None)

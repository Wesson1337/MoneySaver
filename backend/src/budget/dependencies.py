import datetime
from dataclasses import dataclass
from typing import Optional

from fastapi import Query

from backend.src.config import Currencies


@dataclass
class IncomeQuery:
    replenishment_account_id: Optional[int] = Query(default=None)
    currency: Optional[Currencies] = Query(default=None)
    created_at_gte: Optional[datetime.datetime] = Query(default=None, example="2022-11-19T11:49:27.702655")

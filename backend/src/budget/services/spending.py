from typing import Optional
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from backend.src.budget.dependencies import SpendingQueryParams
from backend.src.budget.models import Spending
from backend.src.utils import apply_query_params_to_select_sql_query


async def get_all_spendings_db(
        query_params: SpendingQueryParams,
        session: AsyncSession,
        user_id: Optional[int] = None,
        receipt_account_id: Optional[int] = None
) -> list[Optional[Spending]]:
    select_sql_query = sa.select(Spending). \
        order_by(Spending.created_at.desc()).order_by(Spending.id.desc()). \
        options(joinedload(Spending.receipt_account)). \
        options(joinedload(Spending.category))
    if user_id:
        select_sql_query = select_sql_query.where(Spending.user_id == user_id)
    if receipt_account_id:
        select_sql_query = select_sql_query.where(Spending.receipt_account_id == receipt_account_id)
    select_sql_query_with_filter = await apply_query_params_to_select_sql_query(
        select_sql_query, query_params, Spending
    )
    result = await session.execute(select_sql_query_with_filter)
    spendings = result.scalars().all()
    return spendings

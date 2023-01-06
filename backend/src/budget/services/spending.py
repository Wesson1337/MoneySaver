from decimal import Decimal
from typing import Optional
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from backend.src.budget.dependencies import SpendingQueryParams
from backend.src.budget.models import Spending, Account
from backend.src.budget.schemas.spending import SpendingSchemaIn
from backend.src.budget.services.account import add_amount_to_account_balance
from backend.src.utils import apply_query_params_to_select_sql_query


async def get_all_spendings_db(
        query_params: SpendingQueryParams,
        session: AsyncSession,
        user_id: Optional[int] = None,
        receipt_account_id: Optional[int] = None
) -> list[Optional[Spending]]:
    select_sql_query = sa.select(Spending). \
        order_by(Spending.created_at.desc()).order_by(Spending.id.desc()). \
        options(joinedload(Spending.receipt_account))
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


async def get_spending_by_id_with_joined_receipt_account(
        spending_id: int,
        session: AsyncSession
) -> Optional[Spending]:
    select_sql_query = sa.select(Spending).where(Spending.id == spending_id). \
        options(joinedload(Spending.receipt_account))
    result = await session.execute(select_sql_query)
    spending = result.scalar_one_or_none()
    return spending


async def create_spending_db(
        spending_data: SpendingSchemaIn,
        receipt_account: Account,
        session: AsyncSession
) -> Spending:
    new_spending = Spending(**spending_data.dict())
    amount_in_account_currency = await add_amount_to_account_balance(
        amount=-Decimal(new_spending.amount),
        account=receipt_account,
        currency=new_spending.currency
    )
    new_spending.amount_in_account_currency_at_creation = amount_in_account_currency

    session.add(new_spending)
    await session.commit()

    spending = await get_spending_by_id_with_joined_receipt_account(new_spending.id, session)
    return spending



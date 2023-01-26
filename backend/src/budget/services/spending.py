from decimal import Decimal
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette.background import BackgroundTasks

from backend.src.budget.dependencies import SpendingQueryParams
from backend.src.budget.models import Spending, Account
from backend.src.budget.schemas.spending import SpendingSchemaIn, SpendingSchemaPatch
from backend.src.budget.services.account import add_amount_to_account_balance
from backend.src.exceptions import NoDataForUpdateException
from backend.src.utils import apply_query_params_to_select_sql_query, update_sql_entity


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
        session: AsyncSession,
        background_tasks: BackgroundTasks
) -> Spending:
    new_spending = Spending(**spending_data.dict())
    amount_in_account_currency = await add_amount_to_account_balance(
        amount=-Decimal(new_spending.amount),
        account=receipt_account,
        currency=new_spending.currency,
        background_tasks=background_tasks
    )
    new_spending.amount_in_account_currency_at_creation = -amount_in_account_currency

    session.add(new_spending)
    await session.commit()

    spending = await get_spending_by_id_with_joined_receipt_account(new_spending.id, session)
    return spending


async def patch_spending_db(
        stored_spending: Spending,
        spending_data: SpendingSchemaPatch,
        session: AsyncSession
) -> Spending:
    spending_data = spending_data.dict(exclude_unset=True)

    if not spending_data:
        raise NoDataForUpdateException()

    if spending_data.get('amount') and stored_spending.amount != spending_data['amount']:
        spending_data = await _change_amount_in_spending_data(stored_spending, spending_data)

    updated_spending = await update_sql_entity(stored_spending, spending_data)
    await session.commit()

    return updated_spending


async def _change_amount_in_spending_data(
        stored_spending: Spending,
        spending_data: dict,
        background_tasks: BackgroundTasks
) -> dict:
    new_and_stored_spending_amount_difference = \
        Decimal(spending_data['amount'] - stored_spending.amount).quantize(Decimal('.01'))
    spending_difference_in_account_currency = await add_amount_to_account_balance(
        amount=-new_and_stored_spending_amount_difference,
        currency=stored_spending.currency,
        account=stored_spending.receipt_account,
        background_tasks=BackgroundTasks
    )
    if stored_spending.currency != stored_spending.receipt_account.currency:
        spending_data['amount_in_account_currency_at_creation'] = \
            Decimal(stored_spending.amount_in_account_currency_at_creation).quantize(Decimal('.01')) - \
            spending_difference_in_account_currency
    else:
        spending_data['amount_in_account_currency_at_creation'] = spending_data['amount']

    return spending_data


async def delete_spending_db(
        spending: Spending,
        session: AsyncSession
) -> None:
    spending.receipt_account.balance += spending.amount_in_account_currency_at_creation
    await session.delete(spending)
    await session.commit()

from decimal import Decimal
from typing import Optional
import sqlalchemy as sa
from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from backend.src import redis
from backend.src.budget.dependencies import IncomeQueryParams
from backend.src.budget.exceptions import AccountBalanceWillGoNegativeException
from backend.src.budget.models import Income, Account
from backend.src.budget.schemas.income import IncomeSchemaIn, IncomeSchemaPatch, IncomeSchemaOut
from backend.src.budget.services.account import get_account_by_id_db, add_amount_to_account_balance
from backend.src.exceptions import NoDataForUpdateException
from backend.src.utils import update_sql_entity, apply_query_params_to_select_sql_query


async def get_incomes_db(
        query_params: IncomeQueryParams,
        user_id: int,
        session: AsyncSession,
        replenishment_account_id: Optional[int] = None
) -> list[Income]:
    select_query = sa.select(Income). \
        where(Income.user_id == user_id). \
        order_by(Income.created_at.desc()). \
        order_by(Income.id.desc()). \
        options(joinedload(Income.replenishment_account))

    if replenishment_account_id:
        select_query = select_query.where(Income.replenishment_account_id == replenishment_account_id)

    select_query_with_filter = await apply_query_params_to_select_sql_query(select_query, query_params, Income)

    result = await session.execute(select_query_with_filter)
    incomes = result.scalars().all()
    return incomes


async def create_income_db(
        income_data: IncomeSchemaIn,
        replenishment_account: Account,
        session: AsyncSession,
        background_tasks: BackgroundTasks
) -> Income:
    new_income = Income(**income_data.dict())
    amount_in_account_currency = await add_amount_to_account_balance(
        amount=Decimal(new_income.amount), account=replenishment_account,
        currency=new_income.currency, background_tasks=background_tasks
    )
    new_income.amount_in_account_currency_at_creation = amount_in_account_currency
    session.add(new_income)

    await session.commit()

    new_income.replenishment_account = replenishment_account
    return new_income


async def get_cached_income(income_id: int) -> Optional[Income]:
    income_key = redis.Keys(sql_model=Income).sql_model_key_by_id(income_id)
    cached_income = await redis.get_cache(income_key)
    account = cached_income['replenishment_account']
    del cached_income['replenishment_account']
    income = Income(**cached_income)
    income.replenishment_account = Account(**account)
    income.replenishment_account_id = account['id']
    return income


async def get_certain_income_by_id(
        income_id: int,
        session: AsyncSession,
        background_tasks: Optional[BackgroundTasks] = None
) -> Income:
    cached_income = await get_cached_income(income_id)
    if cached_income is not None:
        return cached_income

    income = await get_income_by_id_with_joined_replenishment_account(income_id, session)
    if income and background_tasks:
        background_tasks.add_task(
            redis.set_cache,
            redis.Keys(sql_model=Income).sql_model_key_by_id(income.id),
            IncomeSchemaOut.from_orm(income).json()
        )
    return income


async def delete_income_db(income: Income, session: AsyncSession) -> None:
    replenishment_account = await get_account_by_id_db(income.replenishment_account_id, session)
    replenishment_account.balance -= income.amount_in_account_currency_at_creation
    if replenishment_account.balance < 0:
        raise AccountBalanceWillGoNegativeException()

    await session.delete(income)
    await session.commit()


async def patch_income_db(
        stored_income: Income,
        income_data: IncomeSchemaPatch,
        session: AsyncSession,
        background_tasks: BackgroundTasks
) -> Income:
    income_data_dict = income_data.dict(exclude_unset=True)

    if not income_data_dict:
        raise NoDataForUpdateException()

    if income_data.amount and income_data.amount != stored_income.amount:
        income_data_dict = await _change_amount_in_income_data(
            stored_income=stored_income,
            income_data=income_data,
            income_data_dict=income_data_dict,
            session=session,
            background_tasks=background_tasks
        )

    updated_income = await update_sql_entity(stored_income, income_data_dict)

    await session.commit()

    return updated_income


async def get_income_by_id_with_joined_replenishment_account(
        income_id: id,
        session: AsyncSession
) -> Optional[Income]:
    # Not using session.get, because we need to execute joinedload in async mode to pass it to pydantic model
    # which is sync
    result = await session.execute(sa.select(Income).
                                   where(Income.id == income_id).
                                   options(joinedload(Income.replenishment_account)))

    income = result.scalar_one_or_none()

    return income


async def _change_amount_in_income_data(
        stored_income: Income,
        income_data: IncomeSchemaPatch,
        income_data_dict: dict,
        session: AsyncSession,
        background_tasks: BackgroundTasks
) -> dict:
    replenishment_account = await get_account_by_id_db(stored_income.replenishment_account_id, session)
    new_and_stored_income_amount_difference = \
        Decimal(income_data.amount).quantize(Decimal('.01')) - \
        Decimal(stored_income.amount).quantize(Decimal('.01'))
    incomes_difference_in_account_currency = await add_amount_to_account_balance(
        amount=new_and_stored_income_amount_difference,
        currency=stored_income.currency,
        account=replenishment_account,
        background_tasks=background_tasks
    )
    if stored_income.currency != replenishment_account.currency:
        income_data_dict['amount_in_account_currency_at_creation'] = \
            Decimal(stored_income.amount_in_account_currency_at_creation).quantize(Decimal('.01')) + \
            incomes_difference_in_account_currency
    else:
        income_data_dict['amount_in_account_currency_at_creation'] = income_data.amount

    return income_data_dict

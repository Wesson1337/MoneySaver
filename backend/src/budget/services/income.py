from decimal import Decimal
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from backend.src.budget.dependencies import IncomeQueryParams
from backend.src.budget.exceptions import IncomeNotFoundException, AccountBalanceWillGoNegativeException
from backend.src.budget.models import Income, Account
from backend.src.budget.schemas.income import IncomeSchemaIn, IncomeSchemaPatch
from backend.src.exceptions import NoDataForUpdateException
from backend.src.utils.service import update_sql_entity, apply_query_params_to_select_sql_query, \
    convert_amount_to_another_currency


async def get_all_incomes_db(session: AsyncSession, query_params: IncomeQueryParams,
                             replenishment_account_id: Optional[int] = None) -> list[Income]:
    select_query = sa.select(Income). \
        order_by(Income.created_at.desc()). \
        order_by(Income.id.desc()). \
        options(joinedload(Income.replenishment_account))

    if replenishment_account_id:
        select_query = select_query.where(Income.replenishment_account_id == replenishment_account_id)

    select_query_with_filter = await apply_query_params_to_select_sql_query(select_query, query_params, Income)

    result = await session.execute(select_query_with_filter)
    incomes = result.scalars().all()
    return incomes


async def create_income_db(income_data: IncomeSchemaIn, session: AsyncSession) -> Income:
    new_income = Income(**income_data.dict())
    session.add(new_income)

    await _add_income_amount_to_account_balance(Decimal(new_income.amount), new_income, session)

    await session.commit()

    income = await _get_income_by_id_with_joined_replenishment_account(income_id=new_income.id, session=session)
    return income


async def get_certain_income_db(income_id: int, session: AsyncSession) -> Income:
    income = await _get_income_by_id_with_joined_replenishment_account(income_id, session)

    return income


async def delete_income_db(income_id: int, session: AsyncSession) -> None:
    income = await session.get(Income, {'id': income_id})

    if not income:
        raise IncomeNotFoundException()

    await _add_income_amount_to_account_balance(Decimal(-income.amount), income, session)

    await session.delete(income)
    await session.commit()


async def patch_income_db(income_id: int,
                          income_data: IncomeSchemaPatch,
                          session: AsyncSession) -> Income:
    income_data_dict = income_data.dict(exclude_unset=True)

    if not income_data_dict:
        raise NoDataForUpdateException()

    stored_income = await _get_income_by_id_with_joined_replenishment_account(income_id, session)

    if income_data.amount and income_data.amount != stored_income.amount:
        new_and_stored_income_amount_difference = Decimal(income_data.amount).quantize(Decimal('.01')) \
                                                  - Decimal(stored_income.amount).quantize(Decimal('.01'))
        await _add_income_amount_to_account_balance(new_and_stored_income_amount_difference, stored_income, session)

    updated_income = await update_sql_entity(income_data_dict, stored_income)

    await session.commit()

    return updated_income


async def _get_income_by_id_with_joined_replenishment_account(income_id: id,
                                                              session: AsyncSession) -> Income:
    # Not using session.get, because we need to execute joinedload in async mode to pass it to pydantic model
    # which is sync
    result = await session.execute(sa.select(Income).
                                   where(Income.id == income_id).
                                   options(joinedload(Income.replenishment_account)))

    try:
        income = result.scalar_one()
    except NoResultFound:
        raise IncomeNotFoundException()

    return income


async def _add_income_amount_to_account_balance(amount: Decimal,
                                                income: Income,
                                                session: AsyncSession) -> None:
    replenishment_account = await session.get(Account, {'id': income.replenishment_account_id})
    if income.currency != replenishment_account.currency:
        amount_in_account_currency = await convert_amount_to_another_currency(
            amount=amount, currency=income.currency, desired_currency=replenishment_account.currency
        )
    else:
        amount_in_account_currency = amount

    replenishment_account.balance += amount_in_account_currency
    if replenishment_account.balance < 0:
        # We can get negative Decimal in func param, so we have to raise exception in that case
        raise AccountBalanceWillGoNegativeException()

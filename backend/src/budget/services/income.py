from decimal import Decimal
from typing import Optional

import sqlalchemy as sa
from asyncpg.exceptions import ForeignKeyViolationError
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from backend.src.budget.dependencies import IncomeQueryParams
from backend.src.budget.exceptions import IncomeNotFoundException
from backend.src.budget.models import Income, Account
from backend.src.budget.schemas.income import IncomeSchemaIn, IncomeSchemaPatch
from backend.src.exceptions import NoDataForUpdateException
from backend.src.utils.service import update_sql_entity, apply_query_params_to_select_query, \
    convert_amount_to_another_currency


async def get_all_incomes_db(session: AsyncSession, query_params: IncomeQueryParams,
                             replenishment_account_id: Optional[int] = None) -> list[Income]:

    select_query = sa.select(Income).\
        order_by(Income.created_at.desc()).\
        order_by(Income.id.desc()).\
        options(joinedload(Income.replenishment_account))

    if replenishment_account_id:
        select_query = select_query.where(Income.replenishment_account_id == replenishment_account_id)

    select_query_with_filter = await apply_query_params_to_select_query(select_query, query_params, Income)

    result = await session.execute(select_query_with_filter)
    incomes = result.scalars().all()
    return incomes


async def create_income_db(income_data: IncomeSchemaIn, session: AsyncSession) -> Income:
    new_income = Income(**income_data.dict())
    session.add(new_income)
    replenishment_account = await session.get(Account, {'id': income_data.replenishment_account_id})
    if not replenishment_account:
        raise HTTPException(status_code=400, detail="Replenishment account not found.")

    await _add_income_amount_to_account_at_creation(new_income, replenishment_account)

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

    await session.delete(income)
    await session.commit()


async def patch_income_db(income_id: int,
                          income_data: IncomeSchemaPatch,
                          session: AsyncSession) -> Income:
    income_data_dict = income_data.dict(exclude_unset=True)

    if not income_data_dict:
        raise NoDataForUpdateException()

    stored_income = await _get_income_by_id_with_joined_replenishment_account(income_id, session)

    try:
        updated_income = await update_sql_entity(income_data_dict, stored_income, session)
    except (ForeignKeyViolationError, IntegrityError):
        raise HTTPException(status_code=400, detail="Replenishment account not found.")

    # TODO add logic to increase/decrease account amount if income amount changes

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


async def _add_income_amount_to_account_at_creation(income: Income, account: Account) -> None:
    income_amount_in_account_currency = account.currency
    if income.currency != account.currency:
        income_amount_in_account_currency = await convert_amount_to_another_currency(
            amount=Decimal(income.amount), currency=income.currency, desired_currency=account.currency
        )

    account.balance += income_amount_in_account_currency

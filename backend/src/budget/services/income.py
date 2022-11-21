import sqlalchemy as sa
from asyncpg.exceptions import ForeignKeyViolationError
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import Select

from backend.src.budget.dependencies import IncomeQueryParams
from backend.src.budget.exceptions import IncomeNotFoundException
from backend.src.budget.models import Income
from backend.src.budget.schemas.income import IncomeSchemaIn


async def _apply_income_filters(select_query: Select, query_params: IncomeQueryParams) -> Select:
    """Applies filters from query parameters to sqlalchemy select query"""

    if query_params.replenishment_account_id:
        select_query = select_query.filter_by(replenishment_account_id=query_params.replenishment_account_id)

    if query_params.currency:
        select_query = select_query.filter_by(currency=query_params.currency)

    if query_params.created_at_gte:
        select_query = select_query.filter(Income.created_at >= query_params.created_at_gte)

    if query_params.created_at_lte:
        select_query = select_query.filter(Income.created_at <= query_params.created_at_lte)

    return select_query


async def get_all_incomes_db(session: AsyncSession, query_params: IncomeQueryParams) -> list[Income]:

    select_query = sa.select(Income).\
        order_by(Income.created_at.desc()).\
        order_by(Income.id.desc()).\
        options(joinedload(Income.replenishment_account))

    select_query = await _apply_income_filters(select_query, query_params)

    result = await session.execute(select_query)
    incomes = result.scalars().all()
    return incomes


async def create_income_db(income_data: IncomeSchemaIn, session: AsyncSession) -> Income:
    new_income = Income(**income_data.dict())
    session.add(new_income)

    try:
        await session.commit()
    except (ForeignKeyViolationError, IntegrityError):
        raise HTTPException(status_code=400, detail="Replenishment account not found.")

    result = await session.execute(sa.select(Income).
                                   where(Income.id == new_income.id).
                                   options(joinedload(Income.replenishment_account)))
    income = result.scalar_one()
    return income


async def get_certain_income_db(income_id: int, session: AsyncSession) -> Income:
    # Not using session.get, because we need to execute joinedload in async mode to pass it to pydantic model
    select_query = sa.select(Income).\
        where(Income.id == income_id).\
        options(joinedload(Income.replenishment_account))\

    result = await session.execute(select_query)

    try:
        income = result.scalar_one()
    except NoResultFound:
        raise IncomeNotFoundException()

    return income


async def delete_income_db(income_id: int, session: AsyncSession) -> None:
    income = await session.get(Income, {'id': income_id})

    if not income:
        raise IncomeNotFoundException()

    await session.delete(income)
    await session.commit()

import sqlalchemy as sa
from asyncpg.exceptions import ForeignKeyViolationError
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import Select

from backend.src.budget.dependencies import IncomeQuery
from backend.src.budget.models import Income
from backend.src.budget.schemas.income import IncomeSchemaIn


async def apply_filters(stmp: Select, query: IncomeQuery) -> Select:
    if query.replenishment_account_id:
        stmp = stmp.filter_by(replenishment_account_id=query.replenishment_account_id)

    if query.currency:
        stmp = stmp.filter_by(currency=query.currency)

    if query.created_at_gte:
        stmp = stmp.filter(Income.created_at >= query.created_at_gte)

    return stmp


async def get_all_incomes_db(session: AsyncSession, query: IncomeQuery) -> list[Income]:

    stmp = sa.select(Income).\
        order_by(Income.created_at.desc()).\
        options(joinedload(Income.replenishment_account))

    stmp = await apply_filters(stmp, query)

    incomes = await session.execute(stmp)
    return incomes.scalars().all()


async def create_income_db(income_data: IncomeSchemaIn, session: AsyncSession) -> Income:
    new_income = Income(**income_data.dict())
    session.add(new_income)

    try:
        await session.commit()
    except (ForeignKeyViolationError, IntegrityError):
        raise HTTPException(status_code=404, detail="Replenishment account not found.")

    new_income = await session.execute(sa.select(Income).
                                       where(Income.id == new_income.id).
                                       options(joinedload(Income.replenishment_account)))
    return new_income.scalar_one()

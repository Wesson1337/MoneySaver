import sqlalchemy as sa
from fastapi import HTTPException
from asyncpg.exceptions import ForeignKeyViolationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from backend.src.budget.models import Income
from backend.src.budget.schemas.income import IncomeSchemaIn


async def get_all_incomes_db(session: AsyncSession) -> list[Income]:
    incomes = await session.execute(sa.select(Income).
                                    order_by(Income.created_at.desc()).
                                    options(joinedload(Income.replenishment_account)))
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

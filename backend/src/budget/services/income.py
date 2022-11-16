import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from backend.src.budget.models import Income


async def get_all_incomes_db(session: AsyncSession) -> list[Income]:
    incomes = await session.execute(sa.select(Income).
                                    order_by(Income.created_at.desc()).
                                    options(joinedload(Income.replenishment_account)))
    return incomes.scalars().all()


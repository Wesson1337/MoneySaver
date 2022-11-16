from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from backend.src.budget.models import Income


async def get_all_incomes_db(session: AsyncSession) -> list[Income]:
    incomes = await session.execute(sa.select(Income).
                                    order_by(Income.created_at.desc()))
    return incomes.scalars.all()


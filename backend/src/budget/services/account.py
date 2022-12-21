from typing import Optional

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.budget.models import Account


async def get_all_accounts_by_user(user_id: int, session: AsyncSession) -> list[Account]:
    result = await session.execute(sa.select(Account).where(Account.user_id == user_id))
    accounts = result.scalars().all()
    return accounts


async def get_account_by_id(account_id: int, session: AsyncSession) -> Optional[Account]:
    result = await session.execute(sa.select(Account).where(Account.id == account_id))
    account = result.scalar_one_or_none()
    return account

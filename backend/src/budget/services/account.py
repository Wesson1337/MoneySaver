from typing import Optional

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.budget.dependencies import AccountQueryParams
from backend.src.budget.models import Account
from backend.src.budget.schemas.account import AccountSchemaIn
from backend.src.utils import apply_query_params_to_select_sql_query


async def get_all_accounts_by_user_db(
        user_id: int,
        query_params: AccountQueryParams,
        session: AsyncSession
) -> list[Account]:
    select_query = sa.select(Account).where(Account.user_id == user_id)
    select_query = await apply_query_params_to_select_sql_query(select_query, query_params, Account)

    result = await session.execute(select_query)
    accounts = result.scalars().all()
    return accounts


async def get_account_by_id(account_id: int, session: AsyncSession) -> Optional[Account]:
    result = await session.execute(sa.select(Account).where(Account.id == account_id))
    account = result.scalar_one_or_none()
    return account


async def create_account_db(account_data: AccountSchemaIn, session: AsyncSession) -> Account:
    new_account = Account(**account_data.dict())

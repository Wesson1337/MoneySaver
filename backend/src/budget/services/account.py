from _decimal import Decimal
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.budget.config import Currencies
from backend.src.budget.dependencies import AccountQueryParams
from backend.src.budget.exceptions import AccountBalanceWillGoNegativeException
from backend.src.budget.models import Account
from backend.src.budget.schemas.account import AccountSchemaIn, AccountSchemaPatch
from backend.src.exceptions import NoDataForUpdateException
from backend.src.utils import apply_query_params_to_select_sql_query, update_sql_entity, \
    convert_amount_to_another_currency


async def get_all_accounts_by_user_db(
        user_id: int,
        query_params: AccountQueryParams,
        session: AsyncSession
) -> list[Account]:
    select_query = sa.select(Account).where(Account.user_id == user_id).\
        order_by(Account.id.desc())
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
    session.add(new_account)
    await session.commit()
    return new_account


async def patch_account_db(
        stored_account: Account,
        account_data: AccountSchemaPatch,
        session: AsyncSession
) -> Account:
    account_data = account_data.dict(exclude_unset=True)
    if not account_data:
        raise NoDataForUpdateException()
    updated_account = await update_sql_entity(sql_entity=stored_account, data_to_update=account_data)
    await session.commit()
    return updated_account


async def add_amount_to_account_balance(
        amount: Decimal,
        currency: Currencies,
        account: Account
) -> Decimal:
    amount_in_account_currency = await convert_amount_to_another_currency(
        amount=amount, currency=currency, desired_currency=account.currency
    )

    account.balance += amount_in_account_currency
    if account.balance < 0:
        # We can get negative Decimal in func param, so we have to raise exception in that case
        raise AccountBalanceWillGoNegativeException()
    return amount_in_account_currency

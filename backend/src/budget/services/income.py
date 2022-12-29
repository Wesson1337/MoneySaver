from decimal import Decimal
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from backend.src.budget.dependencies import IncomeQueryParams
from backend.src.budget.exceptions import AccountBalanceWillGoNegativeException
from backend.src.budget.models import Income, Account
from backend.src.budget.schemas.income import IncomeSchemaIn, IncomeSchemaPatch
from backend.src.budget.services.account import get_account_by_id
from backend.src.config import Currencies
from backend.src.exceptions import NoDataForUpdateException
from backend.src.utils import update_sql_entity, apply_query_params_to_select_sql_query, \
    convert_amount_to_another_currency


async def get_incomes_db(
        query_params: IncomeQueryParams,
        user_id: int,
        session: AsyncSession,
        replenishment_account_id: Optional[int] = None
) -> list[Income]:
    select_query = sa.select(Income). \
        where(Income.user_id == user_id). \
        order_by(Income.created_at.desc()). \
        order_by(Income.id.desc()). \
        options(joinedload(Income.replenishment_account))

    if replenishment_account_id:
        select_query = select_query.where(Income.replenishment_account_id == replenishment_account_id)

    select_query_with_filter = await apply_query_params_to_select_sql_query(select_query, query_params, Income)

    result = await session.execute(select_query_with_filter)
    incomes = result.scalars().all()
    return incomes


async def create_income_db(
        income_data: IncomeSchemaIn,
        replenishment_account: Account,
        session: AsyncSession
) -> Income:
    new_income = Income(**income_data.dict())
    amount_in_account_currency = await _add_income_amount_to_account_balance(
        amount=Decimal(new_income.amount), replenishment_account=replenishment_account,
        income_currency=new_income.currency
    )
    new_income.amount_in_account_currency_at_creation = amount_in_account_currency
    session.add(new_income)

    await session.commit()

    income = await _get_income_by_id_with_joined_replenishment_account(
        income_id=new_income.id, session=session
    )
    return income


async def get_certain_income_by_id(income_id: int, session: AsyncSession) -> Income:
    income = await _get_income_by_id_with_joined_replenishment_account(income_id, session)

    return income


async def delete_income_db(income: Income, session: AsyncSession) -> None:
    replenishment_account = await get_account_by_id(income.replenishment_account_id, session)
    replenishment_account.balance -= income.amount_in_account_currency_at_creation
    if replenishment_account.balance < 0:
        # We can get negative Decimal in func param, so we have to raise exception in that case
        raise AccountBalanceWillGoNegativeException()

    await session.delete(income)
    await session.commit()


async def patch_income_db(
        stored_income: Income,
        income_data: IncomeSchemaPatch,
        session: AsyncSession
) -> Income:
    income_data_dict = income_data.dict(exclude_unset=True)

    if not income_data_dict:
        raise NoDataForUpdateException()

    if income_data.amount and income_data.amount != stored_income.amount:
        income_data_dict = await _change_amount_in_income_data(
            stored_income=stored_income,
            income_data=income_data,
            income_data_dict=income_data_dict,
            session=session
        )

    updated_income = await update_sql_entity(stored_income, income_data_dict)

    await session.commit()

    return updated_income


async def _get_income_by_id_with_joined_replenishment_account(
        income_id: id,
        session: AsyncSession
) -> Optional[Income]:
    # Not using session.get, because we need to execute joinedload in async mode to pass it to pydantic model
    # which is sync
    result = await session.execute(sa.select(Income).
                                   where(Income.id == income_id).
                                   options(joinedload(Income.replenishment_account)))

    income = result.scalar_one_or_none()

    return income


async def _change_amount_in_income_data(
        stored_income: Income,
        income_data: IncomeSchemaPatch,
        income_data_dict: dict,
        session: AsyncSession
) -> dict:
    replenishment_account = await get_account_by_id(stored_income.replenishment_account_id, session)
    new_and_stored_income_amount_difference = \
        Decimal(income_data.amount).quantize(Decimal('.01')) - \
        Decimal(stored_income.amount).quantize(Decimal('.01'))
    incomes_difference_in_account_currency = await _add_income_amount_to_account_balance(
        amount=new_and_stored_income_amount_difference,
        income_currency=stored_income.currency,
        replenishment_account=replenishment_account,
    )
    if stored_income.currency != replenishment_account.currency:
        income_data_dict['amount_in_account_currency_at_creation'] = \
            Decimal(stored_income.amount_in_account_currency_at_creation).quantize(Decimal('.01')) + \
            incomes_difference_in_account_currency
    else:
        income_data_dict['amount_in_account_currency_at_creation'] = income_data.amount

    return income_data_dict


async def _add_income_amount_to_account_balance(
        amount: Decimal,
        income_currency: Currencies,
        replenishment_account: Account
) -> Decimal:
    amount_in_account_currency = await convert_amount_to_another_currency(
        amount=amount, currency=income_currency, desired_currency=replenishment_account.currency
    )

    replenishment_account.balance += amount_in_account_currency
    if replenishment_account.balance < 0:
        # We can get negative Decimal in func param, so we have to raise exception in that case
        raise AccountBalanceWillGoNegativeException()
    return amount_in_account_currency

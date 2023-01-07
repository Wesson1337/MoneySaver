from datetime import datetime, timedelta
from decimal import Decimal

import pytest
import sqlalchemy as sa
from sqlalchemy.sql import Select

from backend.src.auth.models import User
from backend.src.budget.config import Currencies
from backend.src.budget.dependencies import IncomeQueryParams
from backend.src.budget.models import Income
from backend.src.exceptions import WrongDataForUpdateException, NoDataForUpdateException, CurrencyNotSupportedException
from backend.src.utils import convert_amount_to_another_currency, update_sql_entity, \
    apply_query_params_to_select_sql_query

pytestmark = pytest.mark.asyncio


async def test_update_sql_entity():
    sql_entity = User(
        email="lol@email.com"
    )
    data_to_update = {
        "email": "test@email.com",
        "hashed_password": "testvalue"
    }
    updated_sql_entity = await update_sql_entity(sql_entity, data_to_update)
    assert updated_sql_entity.email == data_to_update['email']
    assert updated_sql_entity.hashed_password == data_to_update['hashed_password']


async def test_update_sql_entity_wrong_data():
    sql_entity = User(
        email="lol@email.com"
    )

    data_to_update = {
        "incorrect_key": "incorrect_value"
    }
    with pytest.raises(WrongDataForUpdateException):
        await update_sql_entity(sql_entity, data_to_update)

    data_to_update = {}
    with pytest.raises(NoDataForUpdateException):
        await update_sql_entity(sql_entity, data_to_update)


def format_sql_query(query: Select) -> str:
    return str(query.compile(compile_kwargs={"literal_binds": True}))


async def test_apply_query_params_to_select_sql_query():
    select_sql_query = sa.select(Income).where(Income.id == 1)
    end_datetime = datetime.now()
    start_datetime = end_datetime - timedelta(days=1)
    query_params = IncomeQueryParams(
        currency=Currencies.RUB,
        created_at_ge=str(start_datetime),
        created_at_le=str(end_datetime)
    )
    updated_select_sql_query = await apply_query_params_to_select_sql_query(select_sql_query, query_params, Income)
    desired_select_sql_query = select_sql_query.\
        where(Income.currency == query_params.currency).\
        where(Income.created_at >= str(query_params.created_at_ge)).\
        where(Income.created_at <= str(query_params.created_at_le))
    assert format_sql_query(updated_select_sql_query) == format_sql_query(desired_select_sql_query)


async def test_convert_amount_to_another_currency():
    amount_in_usd = Decimal(5.0)
    amount_in_rub = await convert_amount_to_another_currency(amount_in_usd, Currencies.USD, Currencies.RUB)

    assert amount_in_rub > amount_in_usd

    new_amount_in_usd = await convert_amount_to_another_currency(amount_in_rub, Currencies.RUB, Currencies.USD)

    assert amount_in_rub > new_amount_in_usd
    assert amount_in_usd == new_amount_in_usd


async def test_convert_amount_to_another_currency_wrong_currencies():
    with pytest.raises(CurrencyNotSupportedException):
        await convert_amount_to_another_currency(Decimal(5.0), "incorrect_currency", Currencies.RUB)
    with pytest.raises(CurrencyNotSupportedException):
        await convert_amount_to_another_currency(Decimal(5.0), Currencies.USD, "incorrect_currency")

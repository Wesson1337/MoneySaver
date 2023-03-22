from dataclasses import fields, Field
from decimal import Decimal
from operator import methodcaller
from typing import Type, Any

from aioredis import Redis
from bs4 import BeautifulSoup
from httpx import AsyncClient
from sqlalchemy.sql import Select

from backend.src.budget.config import Currencies
from backend.src.database import Base
from backend.src.dependencies import BaseQueryParams
from backend.src.exceptions import NoDataForUpdateException, WrongDataForUpdateException, CurrencyNotSupportedException
from backend.src.redis import RedisService, Keys

PREFIXES_AND_METHODS = {"_ge": "__ge__", "_le": "__le__", "_ne": "__ne__"}


async def update_sql_entity(sql_entity: Type[Base], data_to_update: dict) -> Type[Base]:
    """Updates sql entity by dict with sql entity attribute as a key, returns sql entity with updated attributes"""
    if not data_to_update:
        raise NoDataForUpdateException()

    for key, value in data_to_update.items():
        if key not in dir(sql_entity):
            raise WrongDataForUpdateException()

        if key is not None and value is not None:
            setattr(sql_entity, key, value)

    return sql_entity


async def apply_query_params_to_select_sql_query(
        select_sql_query: Select,
        query_params: Type[BaseQueryParams],
        sql_table: Type[Base]
) -> Select:
    """Applies query params to sql select query, using filter_by from sqlalchemy.
    To apply query specific params such as 'greater than' or 'lower than' use syntax in the end of an
    attribute of pydantic model:
    >= = _ge
    <= = _le
    != = _ne

    example: created_at_ge
    """

    for query_field in fields(query_params):
        query_field_name = query_field.name
        query_field_value = getattr(query_params, query_field_name)

        if query_field_value is not None:
            prefix_and_method = _get_method_for_specific_field(query_field)
            if prefix_and_method:
                select_sql_query = await _apply_specific_param_to_select_query(
                    query_field_name, query_field_value, prefix_and_method[0],
                    prefix_and_method[1], select_sql_query, sql_table
                )
            else:
                table_attr = getattr(sql_table, query_field_name)
                select_sql_query = select_sql_query.filter(table_attr == query_field_value)

    return select_sql_query


async def _apply_specific_param_to_select_query(
        field_name: str,
        field_value: Any,
        prefix: str,
        method: str, select_sql_query: Select,
        sql_table: Type[Base]
) -> Select:
    field_without_prefix = field_name[:-len(prefix)]
    compare_table_attr_with_value = methodcaller(method, field_value)
    table_attr = getattr(sql_table, field_without_prefix)

    select_sql_query = select_sql_query.filter(compare_table_attr_with_value(table_attr))
    return select_sql_query


def _get_method_for_specific_field(field: Field) -> tuple[str]:
    for prefix, method in PREFIXES_AND_METHODS.items():
        if field.name.endswith(prefix):
            return prefix, method


async def _parse_current_exchange_rate(currency, desired_currency) -> Decimal:
    async with AsyncClient(
            base_url=f'https://investing.com/currencies/{currency.lower()}-{desired_currency.lower()}') as client:
        response = await client.get(url='/', timeout=10, follow_redirects=True)
    soup = BeautifulSoup(response.read(), 'html.parser')
    return Decimal(soup.find("main").find("span", {"data-test": "instrument-price-last"}).text.strip())


async def get_current_exchange_rate(currency, desired_currency, redis) -> Decimal:
    supported_currencies = [field.value for field in Currencies]
    if currency not in supported_currencies:
        raise CurrencyNotSupportedException(currency)
    if desired_currency not in supported_currencies:
        raise CurrencyNotSupportedException(desired_currency)

    cached_rate = await RedisService(redis).get_cache(Keys().currency_key(currency, desired_currency))
    if cached_rate is None:
        rate = await _parse_current_exchange_rate(currency, desired_currency)
        await RedisService(redis).set_cache(
            key=Keys().currency_key(currency, desired_currency),
            data={"rate": float(rate)},
            ex=60 * 60 * 3  # 3 hours
        )
        reversed_rate = (Decimal(1) / rate).quantize(Decimal(".00001"))
        await RedisService(redis).set_cache(
            key=Keys().currency_key(desired_currency, currency),
            data={"rate": float(reversed_rate)},
            ex=60 * 60 * 3
        )
    else:
        rate = cached_rate.get('rate')
    return Decimal(rate)


async def convert_amount_to_another_currency(
        amount: Decimal | float | int,
        currency: Currencies | str,
        desired_currency: Currencies | str,
        redis: Redis
) -> Decimal:
    if currency == desired_currency:
        return amount

    rate = await get_current_exchange_rate(currency, desired_currency, redis)
    return (Decimal(amount) * rate).quantize(Decimal(".01"))



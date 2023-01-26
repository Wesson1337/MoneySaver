import os
from dataclasses import fields, Field
from decimal import Decimal
from operator import methodcaller
from typing import Type, Any

from httpx import AsyncClient
from pydantic import BaseModel
from sqlalchemy.sql import Select

from backend.src.budget.config import Currencies
from backend.src.database import Base
from backend.src.dependencies import BaseQueryParams
from backend.src.exceptions import NoDataForUpdateException, WrongDataForUpdateException, CurrencyNotSupportedException

PREFIXES_AND_METHODS = {"_ge": "__ge__", "_le": "__le__", "_ne": "__ne__"}


class BaseORMSchema(BaseModel):
    class Config:
        orm_mode = True


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


async def convert_amount_to_another_currency(
        amount: Decimal | float | int,
        currency: Currencies | str,
        desired_currency: Currencies | str
) -> Decimal:
    """Converts amount to another currency. It's using https://app.freecurrencyapi.com/.
    Returns a decimal object with two digits after the dot"""
    supported_currencies = [field.value for field in Currencies]
    if currency not in supported_currencies:
        raise CurrencyNotSupportedException(currency)
    if desired_currency not in supported_currencies:
        raise CurrencyNotSupportedException(desired_currency)
    if currency == desired_currency:
        return amount

    amount = Decimal(amount)
    async with AsyncClient(base_url='https://api.freecurrencyapi.com/v1/latest') as client:
        query_params = [('apikey', os.getenv('CURRENCY_API_KEY')),
                        ('base_currency', currency)]
        response = await client.get(url='/', params=query_params, timeout=10)
        desired_currency_rate = response.json()['data'][desired_currency]
        amount_in_desired_currency = amount * Decimal(desired_currency_rate)
        return Decimal(amount_in_desired_currency).quantize(Decimal('.01'))



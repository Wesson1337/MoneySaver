from dataclasses import fields
from decimal import Decimal
from operator import methodcaller
from typing import Type, Any

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from backend.src.config import Currencies
from backend.src.database import Base
from backend.src.dependencies import BaseQueryParams
from backend.src.exceptions import NoDataForUpdateException


async def update_sql_entity(data: dict, sql_entity: Base, session: AsyncSession) -> Base:
    """Updates sql entity by dict with sql entity attribute as a key, returns sql entity with updated attributes"""
    if not data:
        raise NoDataForUpdateException()

    for key, value in data.items():
        if key and value:
            setattr(sql_entity, key, value)

    await session.commit()

    return sql_entity


async def apply_query_params_to_select_query(select_query: Select,
                                             query_params: Type[BaseQueryParams],
                                             sql_table: Type[Base]) -> Select:
    """Applies query params to sql select query, using filter_by from sqlalchemy.
    To apply query specific params such as 'greater than' or 'lower than' use syntax in the end of an
    attribute of pydantic model:
    >= = _ge
    <= = _le
    != = _ne

    example: created_at_ge
    """
    prefixes_and_methods = {"_ge": "__ge__", "_le": "__le__", "_ne": "__ne__"}

    for field in fields(query_params):
        field_name = field.name
        field_value = getattr(query_params, field_name)
        param_is_specific = False

        if field_value:
            for prefix, method in prefixes_and_methods.items():
                if field_name.endswith(prefix):
                    select_query = await _apply_specific_param_to_select_query(field_name, field_value, prefix,
                                                                               method, select_query, sql_table)
                    param_is_specific = True
                    break
            if not param_is_specific:
                table_attr = getattr(sql_table, field_name)
                select_query = select_query.filter(table_attr == field_value)

    return select_query


async def _apply_specific_param_to_select_query(field_name: str, field_value: Any, prefix: str, method: str,
                                                select_query: Select, sql_table: Type[Base]) -> Select:
    field_without_prefix = field_name[:-len(prefix)]
    compare_table_attr_with_value = methodcaller(method, field_value)
    table_attr = getattr(sql_table, field_without_prefix)

    select_query = select_query.filter(compare_table_attr_with_value(table_attr))
    return select_query


async def convert_amount_to_another_currency(amount: Decimal,
                                             currency: Currencies | str,
                                             desired_currency: Currencies | str) -> Decimal:
    async with AsyncClient(base_url='https://api.api-ninjas.com/v1/convertcurrency') as client:
        query_params = [('have', currency), ('want', desired_currency), ('amount', '{:.2f}'.format(amount))]
        response = await client.get(url='/', params=query_params, timeout=10)
        print(response.json())
        amount_in_desired_currency = response.json()['new_amount']
        return amount_in_desired_currency


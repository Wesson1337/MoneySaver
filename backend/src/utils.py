from dataclasses import fields
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from backend.src.database import Base
from backend.src.dependencies import BaseQueryParams
from backend.src.exceptions import NoDataForUpdateException


async def update_sql_model(data: dict, sql_entity: Base, session: AsyncSession) -> Base:
    """Updates sql model by dict with sql entity attribute as a key, returns sql model with updated attributes"""
    if not data:
        raise NoDataForUpdateException()

    for key, value in data.items():
        if key and value:
            setattr(sql_entity, key, value)

    await session.commit()

    return sql_entity


async def apply_query_params_to_select_query(select_query: Select,
                                             query_params: Type[BaseQueryParams],
                                             sql_model: Type[Base]) -> Select:
    """Applies query params to sql select query, using filter_by from sqlalchemy.
    To apply query special params such as 'greater than' or 'lower than' use syntax in the end of an
    attribute of pydantic model:
    >= = _gte
    <= = _lte

    example: created_at_gte
    """
    for attr, value in fields(query_params):
        if attr.endswith('gte'):
            select_query = select_query.filter(getattr(sql_model, attr) >= value)
        if attr.endswith('lte'):
            select_query = select_query.filter(getattr(sql_model, attr) <= value)
        else:
            select_query = select_query.filter(getattr(sql_model, attr) == value)

    return select_query

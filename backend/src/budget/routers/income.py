from typing import List, Literal

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.budget.dependencies import IncomeQueryParams
from backend.src.budget.models import Income
from backend.src.budget.schemas.income import IncomeSchemaOut, IncomeSchemaIn
from backend.src.budget.services.income import get_all_incomes_db, create_income_db, delete_income_db, \
    get_certain_income_db
from backend.src.dependencies import get_async_session

router = APIRouter()


@router.get('/', response_model=List[IncomeSchemaOut])
async def get_all_incomes(query_params: IncomeQueryParams = Depends(),
                          session: AsyncSession = Depends(get_async_session)) -> List[Income]:
    incomes = await get_all_incomes_db(session, query_params)
    return incomes


@router.post('/', response_model=IncomeSchemaOut)
async def create_income(income_data: IncomeSchemaIn,
                        session: AsyncSession = Depends(get_async_session)) -> Income:
    new_income = await create_income_db(income_data, session)
    return new_income


@router.get('/{income_id}', response_model=IncomeSchemaOut)
async def get_certain_income(income_id: int,
                             session: AsyncSession = Depends(get_async_session)) -> Income:
    income = await get_certain_income_db(income_id, session)
    return income


@router.delete('/{income_id}')
async def delete_income(income_id: int,
                        session: AsyncSession = Depends(get_async_session)
                        ) -> dict[Literal["message"], Literal["done"]]:

    await delete_income_db(income_id, session)
    return {"message": "done"}


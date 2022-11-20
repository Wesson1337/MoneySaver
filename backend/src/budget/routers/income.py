from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.budget.dependencies import IncomeQuery
from backend.src.budget.models import Income
from backend.src.budget.schemas.income import IncomeSchemaOut, IncomeSchemaIn
from backend.src.budget.services.income import get_all_incomes_db, create_income_db
from backend.src.dependencies import get_async_session

router = APIRouter()


@router.get('/', response_model=List[IncomeSchemaOut])
async def get_all_incomes(query: IncomeQuery = Depends(),
                          session: AsyncSession = Depends(get_async_session)) -> List[Income]:
    incomes = await get_all_incomes_db(session, query)
    return incomes


@router.post('/', response_model=IncomeSchemaOut)
async def create_income(income_data: IncomeSchemaIn, session: AsyncSession = Depends(get_async_session)) -> Income:
    new_income = await create_income_db(income_data, session)
    return new_income

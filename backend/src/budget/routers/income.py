from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.budget.schemas.income import IncomeSchemaOut
from backend.src.budget.services.income import get_all_incomes_db
from backend.src.dependencies import get_async_session

router = APIRouter()


@router.get('/', response_model=IncomeSchemaOut)
async def get_all_incomes(session: AsyncSession = Depends(get_async_session)):
    incomes = await get_all_incomes_db(session)
    return incomes

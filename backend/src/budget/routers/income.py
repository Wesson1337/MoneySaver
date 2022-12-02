from typing import List, Literal

from asyncpg import ForeignKeyViolationError
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from backend.src.budget.dependencies import IncomeQueryParams
from backend.src.budget.models import Income
from backend.src.budget.schemas.income import IncomeSchemaOut, IncomeSchemaIn, IncomeSchemaPatch
from backend.src.budget.services.income import get_all_incomes_db, create_income_db, delete_income_db, \
    get_certain_income_db, patch_income_db
from backend.src.dependencies import get_async_session

router = APIRouter()


@router.get('/incomes/', response_model=List[IncomeSchemaOut])
async def get_all_incomes(query_params: IncomeQueryParams = Depends(),
                          session: AsyncSession = Depends(get_async_session)) -> List[Income]:
    incomes = await get_all_incomes_db(session, query_params)
    return incomes


@router.get('/accounts/{account_id}/incomes/', response_model=List[IncomeSchemaOut])
async def get_all_incomes_by_account(account_id: int,
                                     query_params: IncomeQueryParams = Depends(),
                                     session: AsyncSession = Depends(get_async_session)) -> List[Income]:
    incomes = await get_all_incomes_db(session, query_params, account_id)
    return incomes


@router.post('/incomes/', response_model=IncomeSchemaOut, status_code=201)
async def create_income(income_data: IncomeSchemaIn,
                        session: AsyncSession = Depends(get_async_session)) -> Income:
    try:
        new_income = await create_income_db(income_data, session)
    except (ForeignKeyViolationError, IntegrityError):
        raise HTTPException(status_code=400, detail="Replenishment account doesn't exists")
    return new_income


@router.get('/incomes/{income_id}/', response_model=IncomeSchemaOut)
async def get_certain_income(income_id: int,
                             session: AsyncSession = Depends(get_async_session)) -> Income:
    income = await get_certain_income_db(income_id, session)
    return income


@router.delete('/incomes/{income_id}/')
async def delete_income(income_id: int,
                        session: AsyncSession = Depends(get_async_session)
                        ) -> dict[Literal["message"], Literal["done"]]:

    await delete_income_db(income_id, session)
    return {"message": "done"}


@router.patch('/incomes/{income_id}/', response_model=IncomeSchemaOut)
async def patch_income(income_id: int,
                       income_data: IncomeSchemaPatch,
                       session: AsyncSession = Depends(get_async_session)) -> Income:
    updated_income = await patch_income_db(income_id, income_data, session)
    return updated_income

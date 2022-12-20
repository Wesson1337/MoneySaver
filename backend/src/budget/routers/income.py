from typing import List, Literal

from asyncpg import ForeignKeyViolationError
from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.auth.dependencies import get_current_active_user
from backend.src.auth.exceptions import NotSuperUserException
from backend.src.auth.models import User
from backend.src.budget.dependencies import IncomeQueryParams
from backend.src.budget.exceptions import ReplenishmentAccountNotExistsException
from backend.src.budget.models import Income
from backend.src.budget.schemas.income import IncomeSchemaOut, IncomeSchemaIn, IncomeSchemaPatch
from backend.src.budget.services.income import create_income_db, delete_income_db, \
    get_certain_income_db, patch_income_db, get_incomes_db
from backend.src.dependencies import get_async_session

router = APIRouter()


@router.get('/users/me/incomes/', response_model=List[IncomeSchemaOut])
async def get_all_incomes_owned_by_current_user(
        query_params: IncomeQueryParams = Depends(),
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session)
) -> List[Income]:
    incomes = await get_incomes_db(session, query_params, current_user.id)
    return incomes


@router.get('/users/{user_id}/incomes/', response_model=List[IncomeSchemaOut])
async def get_all_incomes_owned_by_certain_user(
        user_id: int,
        query_params: IncomeQueryParams = Depends(),
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session)
) -> List[Income]:
    if user_id != current_user.id and not current_user.is_superuser:
        raise NotSuperUserException()
    incomes = await get_incomes_db(session, query_params, user_id)
    return incomes


@router.get('/users/me/accounts/{account_id}/incomes/', response_model=List[IncomeSchemaOut])
async def get_all_incomes_by_account_owned_by_current_user(
        account_id: int,
        query_params: IncomeQueryParams = Depends(),
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session)
) -> List[Income]:
    incomes = await get_incomes_db(session, query_params, current_user.id, account_id)
    return incomes


@router.get('/users/{user_id}/accounts/{account_id}/incomes/', response_model=List[IncomeSchemaOut])
async def get_all_incomes_by_account_owned_by_certain_user(
        account_id: int,
        user_id: int,
        query_params: IncomeQueryParams = Depends(),
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session)
) -> List[Income]:
    if user_id != current_user.id and not current_user.is_superuser:
        raise NotSuperUserException()

    incomes = await get_incomes_db(session, query_params, user_id, account_id)
    return incomes


@router.post('/users/me/incomes/', response_model=IncomeSchemaOut, status_code=201)
async def create_income_for_current_user(
        income_data: IncomeSchemaIn,
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session)
) -> Income:
    try:
        new_income = await create_income_db(income_data, current_user.id, session)
    except (ForeignKeyViolationError, IntegrityError):
        raise ReplenishmentAccountNotExistsException()
    return new_income


@router.post('/users/{user_id}/incomes/', response_model=IncomeSchemaOut, status_code=201)
async def create_income_for_certain_user(
        income_data: IncomeSchemaIn,
        user_id: int,
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session)
) -> Income:
    if user_id != current_user.id and not current_user.is_superuser:
        raise NotSuperUserException
    try: 
        new_income = await create_income_db(income_data, user_id, session)
    except (ForeignKeyViolationError, IntegrityError):
        raise ReplenishmentAccountNotExistsException()
    return new_income


@router.get('/users/me/incomes/{income_id}/', response_model=IncomeSchemaOut)
async def get_certain_income_owned_by_current_user(
        income_id: int,
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session)
) -> Income:
    income = await get_certain_income_db(income_id, current_user.id, session)

    return income


@router.get('/users/{user_id}/incomes/{income_id}', response_model=IncomeSchemaOut)
async def get_certain_income_owned_by_certain_user(
        income_id: int,
        user_id: int,
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session)
) -> Income:
    if user_id != current_user.id and not current_user.is_superuser:
        raise NotSuperUserException()
    
    income = await get_certain_income_db(income_id, user_id, session)

    return income


@router.delete('/users/me/incomes/{income_id}/')
async def delete_income_owned_by_current_user(
        income_id: int,
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session)
) -> dict[Literal["message"], Literal["success"]]:
    await delete_income_db(income_id, current_user.id, session)
    return {"message": "success"}


@router.delete('/users/{user_id}/incomes/{income_id}/')
async def delete_income_owned_by_certain_user(
        income_id: int,
        user_id: int,
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session)
) -> dict[Literal["message"], Literal["success"]]:
    if user_id != current_user.id and not current_user.is_superuser:
        raise NotSuperUserException()

    await delete_income_db(income_id, user_id, session)
    return {"message": "success"}


@router.patch('/users/me/incomes/{income_id}/', response_model=IncomeSchemaOut)
async def patch_income_owned_by_current_user(
        income_id: int,
        income_data: IncomeSchemaPatch,
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session)
) -> Income:
    updated_income = await patch_income_db(income_id, current_user.id, income_data, session)
    return updated_income


@router.patch('/users/{user_id}/incomes/{income_id}/', response_model=IncomeSchemaOut)
async def patch_income_owned_by_certain_user(
        income_id: int,
        user_id: int,
        income_data: IncomeSchemaPatch,
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session)
) -> Income:
    if user_id != current_user.id and not current_user.is_superuser:
        raise NotSuperUserException()

    updated_income = await patch_income_db(income_id, user_id, income_data, session)
    return updated_income

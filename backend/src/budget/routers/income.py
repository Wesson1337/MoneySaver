from typing import List, Literal

from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.auth.dependencies import get_current_active_user
from backend.src.auth.exceptions import NotSuperUserException
from backend.src.auth.models import User
from backend.src.budget.dependencies import IncomeQueryParams
from backend.src.budget.exceptions import ReplenishmentAccountNotExistsException, UserNotExistsException, \
    IncomeNotFoundException, AccountNotFoundException
from backend.src.budget.models import Income
from backend.src.budget.schemas.income import IncomeSchemaOut, IncomeSchemaIn, IncomeSchemaPatch
from backend.src.budget.services.account import get_certain_account_db
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
    incomes = await get_incomes_db(query_params, current_user.id, session)
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
    incomes = await get_incomes_db(query_params, user_id, session)
    return incomes


@router.get('/accounts/{account_id}/incomes/', response_model=List[IncomeSchemaOut])
async def get_all_incomes_by_account(
        account_id: int,
        query_params: IncomeQueryParams = Depends(),
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session)
) -> List[Income]:
    if not current_user.is_superuser:
        account = await get_certain_account_db(account_id, session)
        if not account:
            raise AccountNotFoundException(account_id)
        if account.user_id != current_user.id:
            raise NotSuperUserException()

    incomes = await get_incomes_db(query_params, current_user.id, session, account_id)
    return incomes


@router.post('/incomes/', response_model=IncomeSchemaOut, status_code=201)
async def create_income(
        income_data: IncomeSchemaIn,
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session)
) -> Income:
    if income_data.user_id != current_user.id and not current_user.is_superuser:
        raise NotSuperUserException()

    try:
        new_income = await create_income_db(income_data, session)
    except IntegrityError as e:
        exc_detail = str(e.orig.args).split('\\n')[1]
        if 'replenishment_account_id' in exc_detail:
            raise ReplenishmentAccountNotExistsException(income_data.replenishment_account_id)
        else:
            raise UserNotExistsException(income_data.user_id)

    return new_income


@router.get('/incomes/{income_id}/', response_model=IncomeSchemaOut)
async def get_certain_income(
        income_id: int,
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session)
) -> Income:
    income = await get_certain_income_db(income_id, session)
    if income.user_id != current_user.id and not current_user.is_superuser:
        raise NotSuperUserException()

    return income


@router.delete('/incomes/{income_id}/')
async def delete_income(
        income_id: int,
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session)
) -> dict[Literal["message"], Literal["success"]]:
    income = await get_certain_income_db(income_id, session)

    if not income:
        raise IncomeNotFoundException(income_id)

    if income.user_id != current_user.id and not current_user.is_superuser:
        raise NotSuperUserException()

    await delete_income_db(income, session)
    return {"message": "success"}


@router.patch('/incomes/{income_id}/', response_model=IncomeSchemaOut)
async def patch_income(
        income_id: int,
        income_data: IncomeSchemaPatch,
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session)
) -> Income:
    income = await get_certain_income_db(income_id, session)
    if not income:
        raise IncomeNotFoundException(income_id)

    if income.user_id != current_user.id and not current_user.is_superuser:
        raise NotSuperUserException()

    updated_income = await patch_income_db(income, income_data, session)
    return updated_income


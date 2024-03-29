from typing import List, Literal

from aioredis import Redis
from fastapi import APIRouter, Depends
from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.auth.dependencies import get_current_active_user
from backend.src.auth.models import User
from backend.src.budget.dependencies import IncomeQueryParams
from backend.src.budget.exceptions import AccountNotExistsException, IncomeNotFoundException, \
    AccountNotFoundException, AccountNotBelongsToUserException
from backend.src.budget.models import Income
from backend.src.budget.schemas.income import IncomeSchemaOut, IncomeSchemaIn, IncomeSchemaPatch
from backend.src.budget.services.account import get_account_by_id_db
from backend.src.budget.services.income import create_income_db, delete_income_db, \
    get_certain_income_by_id, patch_income_db, get_income_by_id_with_joined_replenishment_account, \
    get_incomes_db
from backend.src.dependencies import get_async_session, init_redis_pool
from backend.src.exceptions import NotSuperUserException
from backend.src.redis import RedisService, Keys

router = APIRouter()


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
    account = await get_account_by_id_db(account_id, session)
    if not account:
        raise AccountNotFoundException(account_id)
    if account.user_id != current_user.id and not current_user.is_superuser:
        raise NotSuperUserException()

    incomes = await get_incomes_db(query_params, account.user_id, session, account_id)
    return incomes


@router.get('/incomes/{income_id}/', response_model=IncomeSchemaOut)
async def get_certain_income(
        income_id: int,
        background_tasks: BackgroundTasks,
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session),
        redis: Redis = Depends(init_redis_pool)
) -> Income:
    income = await get_certain_income_by_id(income_id, session, background_tasks, redis)
    if not income:
        raise IncomeNotFoundException(income_id)
    if income.user_id != current_user.id and not current_user.is_superuser:
        raise NotSuperUserException()

    return income


@router.post('/incomes/', response_model=IncomeSchemaOut, status_code=201)
async def create_income(
        income_data: IncomeSchemaIn,
        background_tasks: BackgroundTasks,
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session),
        redis: Redis = Depends(init_redis_pool)
) -> Income:
    if income_data.user_id != current_user.id and not current_user.is_superuser:
        raise NotSuperUserException()

    replenishment_account = await get_account_by_id_db(income_data.replenishment_account_id, session)
    if not replenishment_account:
        raise AccountNotExistsException(income_data.replenishment_account_id)
    if replenishment_account.user_id != income_data.user_id:
        raise AccountNotBelongsToUserException(income_data.replenishment_account_id, income_data.user_id)

    new_income = await create_income_db(income_data, replenishment_account, session, background_tasks, redis)
    background_tasks.add_task(
        RedisService(redis).set_cache,
        Keys(sql_model=Income).sql_model_key_by_id(new_income.id),
        IncomeSchemaOut.from_orm(new_income).json()
    )

    return new_income


@router.delete('/incomes/{income_id}/')
async def delete_income(
        income_id: int,
        background_tasks: BackgroundTasks,
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session),
        redis: Redis = Depends(init_redis_pool)
) -> dict[Literal["message"], Literal["success"]]:
    income = await get_income_by_id_with_joined_replenishment_account(income_id, session)

    if not income:
        raise IncomeNotFoundException(income_id)

    if income.user_id != current_user.id and not current_user.is_superuser:
        raise NotSuperUserException()

    await delete_income_db(income, session, background_tasks, redis)
    await redis.delete(Keys(sql_model=Income).sql_model_key_by_id(income_id))
    return {"message": "success"}


@router.patch('/incomes/{income_id}/', response_model=IncomeSchemaOut)
async def patch_income(
        income_id: int,
        income_data: IncomeSchemaPatch,
        background_tasks: BackgroundTasks,
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session),
        redis: Redis = Depends(init_redis_pool)
) -> Income:
    stored_income = await get_income_by_id_with_joined_replenishment_account(income_id, session)
    if not stored_income:
        raise IncomeNotFoundException(income_id)

    if stored_income.user_id != current_user.id and not current_user.is_superuser:
        raise NotSuperUserException()

    updated_income = await patch_income_db(stored_income, income_data, session, background_tasks, redis)
    background_tasks.add_task(
        RedisService(redis).set_cache,
        Keys(sql_model=Income).sql_model_key_by_id(income_id),
        IncomeSchemaOut.from_orm(updated_income).json()
    )
    return updated_income


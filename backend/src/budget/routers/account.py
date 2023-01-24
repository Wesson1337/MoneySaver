from typing import Optional

from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src import redis
from backend.src.auth.dependencies import get_current_active_user
from backend.src.auth.models import User
from backend.src.budget.dependencies import AccountQueryParams
from backend.src.budget.exceptions import AccountNotFoundException, UserNotExistsException
from backend.src.budget.models import Account
from backend.src.budget.schemas.account import AccountSchemaOut, AccountSchemaIn, AccountSchemaPatch
from backend.src.budget.services.account import get_all_accounts_by_user_db, get_account_by_id_db, create_account_db, \
    patch_account_db, get_cached_account_by_id, get_all_cached_accounts_by_user
from backend.src.dependencies import get_async_session
from backend.src.exceptions import NotSuperUserException

router = APIRouter()


@router.get('/users/{user_id}/accounts/', response_model=list[Optional[AccountSchemaOut]])
async def get_all_accounts_by_user(
        user_id: int,
        query_params: AccountQueryParams = Depends(),
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session)
) -> list[Optional[Account]]:
    if user_id != current_user.id and not current_user.is_superuser:
        raise NotSuperUserException()
    cached_accounts = await get_all_cached_accounts_by_user(user_id, query_params)
    if cached_accounts is not None:
        return cached_accounts

    accounts = await get_all_accounts_by_user_db(user_id, query_params, session)
    return accounts


@router.get('/accounts/{account_id}/', response_model=AccountSchemaOut)
async def get_certain_account(
        account_id: int,
        background_tasks: BackgroundTasks,
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session)
) -> Account:
    cached_account = await get_cached_account_by_id(account_id)
    if cached_account is not None:
        if cached_account.user_id != current_user.id and not current_user.is_superuser:
            raise NotSuperUserException()
        return cached_account

    account = await get_account_by_id_db(account_id, session)
    if not account:
        raise AccountNotFoundException(account_id)
    if account.user_id != current_user.id and not current_user.is_superuser:
        raise NotSuperUserException()
    background_tasks.add_task(
        redis.set_cache,
        redis.Keys(sql_model=Account).sql_model_key_by_id(account_id),
        AccountSchemaOut.from_orm(account).json()
    )
    return account


@router.post('/accounts/', status_code=201, response_model=AccountSchemaOut)
async def create_account(
        account_data: AccountSchemaIn,
        background_tasks: BackgroundTasks,
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session)
) -> Account:
    if account_data.user_id != current_user.id and not current_user.is_superuser:
        raise NotSuperUserException()
    try:
        account = await create_account_db(account_data, session)
    except IntegrityError as e:
        raise UserNotExistsException(account_data.user_id)
    background_tasks.add_task(
        redis.set_cache,
        redis.Keys(sql_model=Account).sql_model_key_by_id(account.id),
        AccountSchemaOut.from_orm(account).json()
    )
    return account


@router.patch('/accounts/{account_id}/', response_model=AccountSchemaOut)
async def patch_account(
        account_id: int,
        account_data: AccountSchemaPatch,
        background_tasks: BackgroundTasks,
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session)
) -> Account:
    stored_account = await get_account_by_id_db(account_id, session)
    if not stored_account:
        raise AccountNotFoundException(account_id=account_id)
    if stored_account.user_id != current_user.id and not current_user.is_superuser:
        raise NotSuperUserException()
    updated_account = await patch_account_db(stored_account, account_data, session)
    background_tasks.add_task(
        redis.set_cache,
        redis.Keys(sql_model=Account).sql_model_key_by_id(updated_account.id),
        AccountSchemaOut.from_orm(updated_account).json()
    )
    return updated_account

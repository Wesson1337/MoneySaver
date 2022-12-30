from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.auth.dependencies import get_current_active_user
from backend.src.auth.models import User
from backend.src.budget.dependencies import AccountQueryParams
from backend.src.budget.exceptions import AccountNotFoundException
from backend.src.budget.models import Account
from backend.src.budget.schemas.account import AccountSchemaOut, AccountSchemaIn
from backend.src.budget.services.account import get_all_accounts_by_user_db, get_account_by_id, create_account_db
from backend.src.dependencies import get_async_session
from backend.src.exceptions import NotSuperUserException

router = APIRouter()


@router.get('/users/{user_id}/accounts/', response_model=list[AccountSchemaOut])
async def get_all_accounts_by_user(
        user_id: int,
        query_params: AccountQueryParams = Depends(),
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session)
) -> list[Account]:
    if user_id != current_user.id and not current_user.is_superuser:
        raise NotSuperUserException()
    accounts = await get_all_accounts_by_user_db(user_id, query_params, session)
    return accounts


@router.get('/accounts/{account_id}/', response_model=AccountSchemaOut)
async def get_certain_account(
        account_id: int,
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session)
) -> Account:
    account = await get_account_by_id(account_id, session)
    if not account:
        raise AccountNotFoundException(account_id)
    if account.user_id != current_user.id and not current_user.is_superuser:
        raise NotSuperUserException()
    return account


@router.post('/accounts/', response_model=AccountSchemaOut)
async def create_account(
        account_data: AccountSchemaIn,
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session)
) -> Account:
    account = create_account_db()
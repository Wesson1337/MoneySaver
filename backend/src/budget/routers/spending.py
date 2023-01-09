from typing import Optional, Literal

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.auth.dependencies import get_current_active_user
from backend.src.auth.models import User
from backend.src.budget.dependencies import SpendingQueryParams
from backend.src.budget.exceptions import AccountNotFoundException, SpendingNotFoundException, \
    AccountNotBelongsToUserException, AccountNotExistsException
from backend.src.budget.models import Spending
from backend.src.budget.schemas.spending import SpendingSchemaOut, SpendingSchemaIn, SpendingSchemaPatch
from backend.src.budget.services.account import get_account_by_id
from backend.src.budget.services.spending import get_all_spendings_db, \
    get_spending_by_id_with_joined_receipt_account, create_spending_db, patch_spending_db, delete_spending_db
from backend.src.dependencies import get_async_session
from backend.src.exceptions import NotSuperUserException

router = APIRouter()


@router.get('/users/{user_id}/spendings/', response_model=list[Optional[SpendingSchemaOut]])
async def get_all_spendings_by_user(
        user_id: int,
        query_params: SpendingQueryParams = Depends(),
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session)
) -> list[Optional[Spending]]:
    if user_id != current_user.id and not current_user.is_superuser:
        raise NotSuperUserException()
    spendings = await get_all_spendings_db(
        user_id=user_id, query_params=query_params, session=session
    )
    return spendings


@router.get('/accounts/{account_id}/spendings/', response_model=list[Optional[SpendingSchemaOut]])
async def get_all_spendings_by_account(
        account_id: int,
        query_params: SpendingQueryParams = Depends(),
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session)
) -> list[Optional[Spending]]:
    account = await get_account_by_id(account_id, session)
    if not account:
        raise AccountNotFoundException(account_id)
    if account.user_id != current_user.id and not current_user.is_superuser:
        raise NotSuperUserException
    spendings = await get_all_spendings_db(
        receipt_account_id=account_id, query_params=query_params, session=session
    )
    return spendings


@router.get('/spendings/{spending_id}/', response_model=SpendingSchemaOut)
async def get_certain_spending(
        spending_id: int,
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session)
) -> Spending:
    spending = await get_spending_by_id_with_joined_receipt_account(spending_id, session)
    if not spending:
        raise SpendingNotFoundException(spending_id)
    if spending.user_id != current_user.id and not current_user.is_superuser:
        raise NotSuperUserException()
    return spending


@router.post('/spendings/', response_model=SpendingSchemaOut)
async def create_spending(
        spending_data: SpendingSchemaIn,
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session)
) -> Spending:
    if spending_data.user_id != current_user.id and not current_user.is_superuser:
        raise NotSuperUserException()
    receipt_account = await get_account_by_id(spending_data.receipt_account_id, session)
    if not receipt_account:
        raise AccountNotExistsException(spending_data.receipt_account_id)
    if receipt_account.user_id != spending_data.user_id:
        raise AccountNotBelongsToUserException(spending_data.receipt_account_id, spending_data.user_id)

    spending = await create_spending_db(spending_data, receipt_account, session)

    return spending


@router.patch('/spendings/{spending_id}/', response_model=SpendingSchemaOut)
async def patch_spending(
        spending_id: int,
        spending_data: SpendingSchemaPatch,
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session)
) -> Spending:
    spending = await get_spending_by_id_with_joined_receipt_account(spending_id, session)
    if not spending:
        raise SpendingNotFoundException(spending_id)
    if spending.user_id != current_user.id and not current_user.is_superuser:
        raise NotSuperUserException()
    updated_spending = await patch_spending_db(spending, spending_data, session)
    return updated_spending


@router.delete('/spendings/{spending_id}/')
async def delete_spending(
        spending_id: int,
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session)
) -> dict[Literal["message"], str]:
    spending = await get_spending_by_id_with_joined_receipt_account(spending_id, session)
    if not spending:
        raise SpendingNotFoundException(spending_id)
    if spending.user_id != current_user.id and not current_user.is_superuser:
        raise NotSuperUserException()
    await delete_spending_db(spending, session)
    return {"message": "success"}

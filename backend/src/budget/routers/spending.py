from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.auth.dependencies import get_current_active_user
from backend.src.auth.models import User
from backend.src.budget.dependencies import SpendingQueryParams
from backend.src.budget.exceptions import AccountNotFoundException
from backend.src.budget.models import Spending
from backend.src.budget.schemas.spending import SpendingSchemaOut
from backend.src.budget.services.account import get_account_by_id
from backend.src.budget.services.spending import get_all_spendings_db
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


from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.auth.dependencies import get_current_active_user
from backend.src.auth.models import User
from backend.src.budget.dependencies import AccountQueryParams
from backend.src.budget.models import Account
from backend.src.budget.schemas.account import AccountSchemaOut
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
    accounts = get_accounts_by_user_db()
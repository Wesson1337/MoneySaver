from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.auth.dependencies import get_current_active_user
from backend.src.auth.models import User
from backend.src.budget.models import Spending
from backend.src.budget.schemas.spending import SpendingSchemaOut
from backend.src.dependencies import get_async_session

router = APIRouter()


@router.get('/users/{user_id}/spendings/', response_model=list[Optional[SpendingSchemaOut]])
async def get_all_spendings_by_user(
        user_id: int,
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session)
) -> list[Optional[Spending]]:
    pass
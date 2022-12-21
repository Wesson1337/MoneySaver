from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

import backend.src.auth.utils as auth_utils
from backend.src.auth import service
from backend.src.auth.config import ACCESS_TOKEN_EXPIRE_MINUTES
from backend.src.auth.dependencies import get_current_active_user
from backend.src.auth.exceptions import IncorrectEmailOrPasswordException
from backend.src.exceptions import NotSuperUserException
from backend.src.auth.models import User
from backend.src.auth.schemas import Token, UserSchemaOut, UserSchemaIn
from backend.src.dependencies import get_async_session

router = APIRouter()


@router.post('/token/', response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 session: AsyncSession = Depends(get_async_session)) -> dict:
    user = await service.authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise IncorrectEmailOrPasswordException()
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_utils.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get('/users/me/', response_model=UserSchemaOut)
async def get_current_user(current_user: User = Depends(get_current_active_user)) -> User:
    return current_user


@router.get('/users/{user_id}/', response_model=UserSchemaOut)
async def get_certain_user(
        user_id: int,
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session)
) -> User:
    if user_id != current_user.id and not current_user.is_superuser:
        raise NotSuperUserException()

    user = await service.get_user_by_id(user_id, session)
    return user


@router.post('/users/', response_model=UserSchemaOut)
async def create_new_user(new_user_data: UserSchemaIn,
                          session: AsyncSession = Depends(get_async_session)):
    new_user = await service.create_user(new_user_data=new_user_data, session=session)
    return new_user


from datetime import timedelta

from aioredis import Redis
from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

import backend.src.auth.utils as auth_utils
from backend.src.auth import service
from backend.src.auth.config import ACCESS_TOKEN_EXPIRE_MINUTES
from backend.src.auth.dependencies import get_current_active_user
from backend.src.auth.exceptions import IncorrectEmailOrPasswordException, EmailAlreadyExistsException, \
    UserNotFoundException
from backend.src.auth.models import User
from backend.src.auth.schemas import Token, UserSchemaOut, UserSchemaIn
from backend.src.dependencies import get_async_session
from backend.src.exceptions import NotSuperUserException
from backend.src.redis import init_redis_pool, RedisService, Keys

router = APIRouter()


@router.post('/token/', response_model=Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    user = await service.authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise IncorrectEmailOrPasswordException()
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_utils.create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get('/users/me/', response_model=UserSchemaOut)
async def get_current_user(current_user: User = Depends(get_current_active_user)) -> User:
    return current_user


@router.get('/users/{user_id}/', response_model=UserSchemaOut)
async def get_certain_user(
        user_id: int,
        background_tasks: BackgroundTasks,
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session),
        redis: Redis = Depends(init_redis_pool)
) -> User:
    if user_id != current_user.id and not current_user.is_superuser:
        raise NotSuperUserException()

    user = await service.get_user_by_id(user_id, session, background_tasks, redis)
    if not user:
        raise UserNotFoundException(user_id)

    return user


@router.post('/users/', response_model=UserSchemaOut)
async def create_new_user(
        new_user_data: UserSchemaIn,
        background_tasks: BackgroundTasks,
        session: AsyncSession = Depends(get_async_session),
        redis: Redis = Depends(init_redis_pool)
) -> User:
    user_with_email_from_new_user_data = await service.get_user_by_email(new_user_data.email, session)
    if user_with_email_from_new_user_data is not None:
        raise EmailAlreadyExistsException(new_user_data.email)

    new_user = await service.create_user(new_user_data, session)
    background_tasks.add_task(
        RedisService(redis).set_cache,
        Keys(sql_model=User).sql_model_key_by_id(new_user.id),
        UserSchemaOut.from_orm(new_user).json()
    )
    return new_user

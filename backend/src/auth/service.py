from typing import Optional

import sqlalchemy as sa
from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

import backend.src.auth.utils as auth_utils
from backend.src import redis
from backend.src.auth.models import User
from backend.src.auth.schemas import UserSchemaIn, UserSchemaOut


async def get_user_by_email(email: str, session: AsyncSession) -> User | None:
    result = await session.execute(sa.select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    return user


async def authenticate_user(email: str, password: str, session: AsyncSession) -> Optional[User]:
    user = await get_user_by_email(email, session)
    if not user:
        return
    if not auth_utils.verify_password(password, user.hashed_password):
        return
    return user


async def get_cached_user_by_id(user_id: int) -> Optional[User]:
    user_key_name = redis.Keys(sql_model=User).sql_model_key_by_id(user_id)
    user = await redis.get_cache(user_key_name)
    if user:
        return User(**user)


async def get_user_by_id_db(user_id: int, session) -> Optional[User]:
    result = await session.execute(sa.select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    return user


async def get_user_by_id(
        user_id: int,
        session: AsyncSession,
        background_tasks: Optional[BackgroundTasks] = None
) -> Optional[User]:
    cached_user = await get_cached_user_by_id(user_id)
    if cached_user is not None:
        return cached_user

    user = await get_user_by_id_db(user_id, session)
    if background_tasks and user:
        background_tasks.add_task(
            redis.set_cache,
            redis.Keys(sql_model=User).sql_model_key_by_id(user_id),
            UserSchemaOut.from_orm(user).json()
        )
    return user


async def create_user(new_user_data: UserSchemaIn, session: AsyncSession) -> User:
    new_user_dict = _change_user_password_to_hashed_password(new_user_data)
    new_user = User(**new_user_dict)
    session.add(new_user)
    await session.commit()

    return new_user


def _change_user_password_to_hashed_password(user_data: UserSchemaIn) -> dict:
    user_dict = user_data.dict()
    hashed_password = auth_utils.get_password_hash(user_data.password1)
    del user_dict['password1']
    del user_dict['password2']
    user_dict.update({'hashed_password': hashed_password})
    return user_dict

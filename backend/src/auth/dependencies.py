from aioredis import Redis
from fastapi import Depends, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.auth.config import JWT_SECRET_KEY, JWT_ALGORITHM
from backend.src.auth.exceptions import CredentialsException, InactiveUserException
from backend.src.auth.models import User
from backend.src.auth.schemas import TokenData, UserSchemaOut
from backend.src.auth.service import get_cached_user_by_id, get_user_by_id_db
from backend.src.config import API_PREFIX_V1
from backend.src.dependencies import get_async_session, init_redis_pool
from backend.src.redis import RedisService, Keys

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{API_PREFIX_V1}/token")


async def get_current_user(
        background_tasks: BackgroundTasks,
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_async_session),
        redis: Redis = Depends(init_redis_pool)
) -> User:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        token_data = TokenData(id=payload.get("sub"))
        user_id = int(token_data.id)
    except (JWTError, ValidationError):
        raise CredentialsException()

    cached_user = await get_cached_user_by_id(user_id, redis)
    if cached_user:
        return cached_user

    user = await get_user_by_id_db(user_id, session)
    if user is None:
        raise CredentialsException()
    if background_tasks:
        background_tasks.add_task(
            RedisService(redis).set_cache,
            Keys(sql_model=User).sql_model_key_by_id(user.id),
            UserSchemaOut.from_orm(user).json()
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise InactiveUserException()
    return current_user

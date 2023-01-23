from fastapi import Depends, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src import redis
from backend.src.auth.config import JWT_SECRET_KEY, JWT_ALGORITHM
from backend.src.auth.exceptions import CredentialsException, InactiveUserException
from backend.src.auth.models import User
from backend.src.auth.schemas import TokenData, UserSchemaOut
from backend.src.auth.service import get_user_by_email, get_cached_user_by_id, get_user_by_id_db
from backend.src.config import DEFAULT_API_PREFIX
from backend.src.dependencies import get_async_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{DEFAULT_API_PREFIX}/token")


async def get_current_user(
        background_tasks: BackgroundTasks,
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_async_session)
) -> User:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id = int(payload.get("sub"))
        if user_id is None:
            raise CredentialsException()
        token_data = TokenData(id=user_id)
    except (JWTError, ValidationError):
        raise CredentialsException()

    cached_user = await get_cached_user_by_id(user_id)
    if cached_user:
        return cached_user

    user = await get_user_by_id_db(user_id, session)
    if user is None:
        raise CredentialsException()
    background_tasks.add_task(
        redis.set_cache,
        redis.Keys(sql_model=User).sql_model_key_by_id(user.id),
        UserSchemaOut.from_orm(user).json()
    )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise InactiveUserException()
    return current_user


import pytest
import sqlalchemy as sa
from aioredis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.auth.config import pwd_context
from backend.src.auth.dependencies import get_current_user, get_current_active_user
from backend.src.auth.exceptions import CredentialsException, InactiveUserException
from backend.src.auth.models import User
from backend.src.tests.conftest import PRELOAD_DATA

pytestmark = pytest.mark.asyncio


async def test_get_current_user(
        ordinary_user_encoded_jwt_token: str,
        superuser_encoded_jwt_token: str,
        session: AsyncSession,
        redis: Redis
):
    cached_user = await get_current_user(
        token=ordinary_user_encoded_jwt_token, session=session, redis=redis, background_tasks=None
    )
    assert isinstance(cached_user, User)
    result = await session.execute(sa.select(User).where(User.id == cached_user.id))
    user_from_db = result.scalar_one()
    assert isinstance(user_from_db, User)
    preload_user_data = PRELOAD_DATA['user_2']['data']
    assert cached_user.is_superuser is preload_user_data['is_superuser']
    assert pwd_context.verify('test_password', user_from_db.hashed_password)

    cached_user = await get_current_user(
        token=superuser_encoded_jwt_token, session=session, redis=redis, background_tasks=None
    )
    assert isinstance(cached_user, User)
    result = await session.execute(sa.select(User).where(User.id == cached_user.id))
    user_from_db = result.scalar_one()
    assert isinstance(user_from_db, User)
    preload_user_data = PRELOAD_DATA['user_1']['data']
    assert cached_user.is_superuser is preload_user_data['is_superuser']
    assert pwd_context.verify('test_password', user_from_db.hashed_password)


@pytest.mark.parametrize('wrong_token', [
    # expired_token
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNTE2MjM5MDIyfQ."
    "-6YUdFgOUkQBqfWx8DmFYVEEvJ0QHCtZ9H9HaPDNuCY",
    # incorrect id
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZmFmZHNmYWZkYWZkcyIsImV4cCI6MjUwMDAwMDAwMH0."
    "tVbH8Ujk75CA7MvgGZWXLi_GB_J0ug9AP-sUkitvRYY",
    # id doesn't exists in db
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMTExMTExMSIsImV4cCI6MjUwMDAwMDAwMH0."
    "rHpSFcN-9MVMwXVzZ_GfGhU8dmV481Xw4g9Jzzyz87c",
    # id not in token
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjI1MDAwMDAwMDB9.4GqxpcvTZBaeRDKtlaxoGgd9PNQpKxFSajNsfuh7wWU"
])
async def test_get_current_user_wrong_data(
        wrong_token: str,
        ordinary_user_encoded_jwt_token: str,
        session: AsyncSession,
        redis: Redis
):
    # checking token didn't change
    user = await get_current_user(
        token=ordinary_user_encoded_jwt_token, background_tasks=None, session=session, redis=redis
    )
    assert isinstance(user, User)
    with pytest.raises(CredentialsException):
        await get_current_user(token=wrong_token, background_tasks=None, session=session, redis=redis)


async def test_get_current_active_user(seed_db, session: AsyncSession):
    result = await session.execute(sa.select(User).where(User.id == 1))
    active_user = result.scalar_one()
    active_user = await get_current_active_user(active_user)
    assert isinstance(active_user, User)


async def test_get_current_active_user_not_active_user(seed_db, session: AsyncSession):
    result = await session.execute(sa.select(User).where(User.id == 3))
    inactive_user = result.scalar_one()
    with pytest.raises(InactiveUserException):
        await get_current_active_user(inactive_user)

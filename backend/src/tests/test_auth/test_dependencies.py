import pytest
import sqlalchemy as sa
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
        session: AsyncSession
):
    user = await get_current_user(ordinary_user_encoded_jwt_token, session)
    assert isinstance(user, User)
    preload_user_data = PRELOAD_DATA['user_2']['data']
    assert user.is_superuser is preload_user_data['is_superuser']
    assert pwd_context.verify('test_password', user.hashed_password)

    user = await get_current_user(superuser_encoded_jwt_token, session)
    assert isinstance(user, User)
    preload_user_data = PRELOAD_DATA['user_1']['data']
    assert user.is_superuser is preload_user_data['is_superuser']
    assert pwd_context.verify('test_password', user.hashed_password)


async def test_get_current_user_wrong_data(seed_db, session: AsyncSession):
    # expired_token
    test_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QGV4YW1wb" \
                 "GUuY29tIiwiZXhwIjoxNTE2MjM5MDIyfQ.5m4TnaDPUPOPQbS9WyT26GBmdRuofYfMfpyWjE6W3Z0"
    with pytest.raises(CredentialsException):
        await get_current_user(test_token, session)

    # incorrect email
    test_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoyOTE2MjM5MDIyfQ" \
                 ".AzjIT55WveIpV9x-sFidG1JmTOJoSrkECJPk_roeh7I"
    with pytest.raises(CredentialsException):
        await get_current_user(test_token, session)

    # email doesn't exists in db
    test_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJub3RfZXhpc3RpbmdfZW1haWxAZXhhbXBsZS5jb20iLCJl" \
                 "eHAiOjI5MTYyMzkwMjJ9.8V5cfUt0z78qa3UkkmjJBULlmRQTjErA_kAAbyUekgE"
    with pytest.raises(CredentialsException):
        await get_current_user(test_token, session)

    # email not in token
    test_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjI5MTYyMzkw" \
                 "MjJ9.hKkJBZ-hyqOeKsOga1kCzSHFnbZDsuWhzH40gkKa6_c"
    with pytest.raises(CredentialsException):
        await get_current_user(test_token, session)


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


# TODO rewrite tests for auth with id instead of email

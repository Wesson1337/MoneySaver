from typing import Literal

import pytest
from httpx import AsyncClient

from backend.src.budget.models import Account
from backend.src.config import DEFAULT_API_PREFIX
from backend.src.tests.conftest import PRELOAD_DATA

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize('user_id', [1, 2])
async def test_get_all_accounts_by_user(
        user_id: int,
        auth_headers_superuser: tuple[Literal["Authorization"], str],
        client: AsyncClient
):
    query_params = [('is_active', True)]
    response = await client.get(
        f'{DEFAULT_API_PREFIX}/budget/users/{user_id}/accounts/',
        headers=[auth_headers_superuser],
        params=query_params
    )
    assert response.status_code == 200
    preloaded_active_accounts = [
        PRELOAD_DATA[name]['data'] for name in PRELOAD_DATA
        if PRELOAD_DATA[name]['model'] == Account
        and PRELOAD_DATA[name]['data']['user_id'] == user_id
        and PRELOAD_DATA[name]['data']['is_active'] is True
    ]
    assert len(response.json()) == len(preloaded_active_accounts)
    print(response.json())
    for account in response.json():
        assert account['user_id'] == user_id



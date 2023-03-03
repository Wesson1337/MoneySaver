from typing import Literal

import pytest
from httpx import AsyncClient

from backend.src.budget.config import Currencies, AccountTypes
from backend.src.budget.exceptions import AccountNotFoundException, UserNotExistsException
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
    for account in response.json():
        assert account['user_id'] == user_id


@pytest.mark.parametrize('incorrect_query', [
    ('is_active', ''),
    ('is_active', 'lol')
])
async def test_get_all_accounts_by_user_incorrect_query(
        incorrect_query: tuple,
        auth_headers_superuser: tuple[Literal["Authorization"], str],
        client: AsyncClient
):
    response = await client.get(
        f'{DEFAULT_API_PREFIX}/budget/users/1/accounts/',
        headers=[auth_headers_superuser],
        params=[incorrect_query]
    )
    assert response.status_code == 422


@pytest.mark.parametrize('account_id', [1, 2])
async def test_get_certain_account(
        account_id: int,
        auth_headers_superuser: tuple[Literal["Authorization"], str],
        client: AsyncClient
):
    response = await client.get(
        f'{DEFAULT_API_PREFIX}/budget/accounts/{account_id}/',
        headers=[auth_headers_superuser]
    )
    assert response.status_code == 200
    preloaded_account = [
        PRELOAD_DATA[name]['data'] for name in PRELOAD_DATA
        if PRELOAD_DATA[name]['model'] == Account
        and name.endswith(str(account_id))
    ][0]

    for key, value in preloaded_account.items():
        assert response.json()[key] == value


async def test_get_certain_nonexistent_account(
        auth_headers_superuser: tuple[Literal["Authorization"], str],
        client: AsyncClient
):
    response = await client.get(
        f'{DEFAULT_API_PREFIX}/budget/accounts/9999/',
        headers=[auth_headers_superuser]
    )
    assert response.status_code == 404
    assert response.json()['detail'] == AccountNotFoundException(9999).detail


async def test_create_account(
        auth_headers_superuser: tuple[Literal["Authorization"], str],
        client: AsyncClient
):
    account_data = {
        "name": "test_account",
        "user_id": 1,
        "type": AccountTypes.BANK_ACCOUNT,
        "currency": Currencies.USD,
        "balance": 0
    }
    response = await client.post(
        f'{DEFAULT_API_PREFIX}/budget/accounts/',
        headers=[auth_headers_superuser],
        json=account_data
    )
    assert response.status_code == 201
    for key, value in account_data.items():
        assert response.json()[key] == value
    assert response.json()['is_active'] is True


@pytest.mark.parametrize('account_data, status_code, detail', [
    ({
        "name": "test_account",
        "user_id": 1,
        "type": "testtest",
        "currency": Currencies.USD,
        "balance": 0
    }, 422, None),
    ({
        "name": "test_account",
        "user_id": 1,
        "type": AccountTypes.BANK_ACCOUNT,
        "currency": "testtest",
        "balance": 0
    }, 422, None),
    ({
        "name": "test_account",
        "user_id": 9999,
        "type": AccountTypes.BANK_ACCOUNT,
        "currency": Currencies.RUB,
        "balance": 0
    }, 400, UserNotExistsException(9999).detail),
    ({
        "name": "test_account",
        "user_id": 1,
        "type": AccountTypes.BANK_ACCOUNT,
        "currency": Currencies.RUB,
        "balance": -1
    }, 422, None),
    ({
        "name": "test_account",
        "user_id": 1,
        "type": AccountTypes.BANK_ACCOUNT,
        "currency": Currencies.USD,
        "balance": 1000000000000
    }, 422, None),
    ({}, 422, None)
])
async def test_create_incorrect_account(
        account_data: dict,
        status_code: int,
        detail: str,
        auth_headers_superuser: tuple[Literal["Authorization"], str],
        client: AsyncClient
):
    response = await client.post(
        f'{DEFAULT_API_PREFIX}/budget/accounts/',
        headers=[auth_headers_superuser],
        json=account_data
    )
    assert response.status_code == status_code
    if detail:
        assert response.json()['detail'] == detail


async def test_patch_account(
        auth_headers_superuser: tuple[Literal["Authorization"], str],
        client: AsyncClient
):
    account_data = {
        "name": "test_account",
        "is_active": True
    }
    response = await client.patch(
        f"{DEFAULT_API_PREFIX}/budget/accounts/1/",
        headers=[auth_headers_superuser],
        json=account_data
    )
    assert response.status_code == 200
    for key, value in account_data.items():
        assert response.json()[key] == value


@pytest.mark.parametrize('account_data, status_code', [
    ({
        "is_active": 'str'
    }, 422),
    ({
        "type": "testtest"
    }, 422),
    ({}, 400)
])
async def test_patch_account_incorrect_data(
        account_data: dict,
        status_code: int,
        auth_headers_superuser: tuple[Literal["Authorization"], str],
        client: AsyncClient
):
    response = await client.patch(
        f"{DEFAULT_API_PREFIX}/budget/accounts/1/",
        headers=[auth_headers_superuser],
        json=account_data
    )
    assert response.status_code == status_code


async def test_patch_nonexistent_account(
        auth_headers_superuser: tuple[Literal["Authorization"], str],
        client: AsyncClient
):
    response = await client.patch(
        f"{DEFAULT_API_PREFIX}/budget/accounts/9999/",
        headers=[auth_headers_superuser],
        json={}
    )
    assert response.status_code == 404
    assert response.json()['detail'] == AccountNotFoundException(9999).detail

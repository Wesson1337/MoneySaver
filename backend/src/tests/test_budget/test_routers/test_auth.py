from typing import Literal

import pytest
from httpx import AsyncClient
from pytest_lazyfixture import lazy_fixture

from backend.src.config import DEFAULT_API_PREFIX, Currencies, AccountTypes

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize('url', [
    '{DEFAULT_API_PREFIX}/budget/users/{user_id}/incomes/',
    '{DEFAULT_API_PREFIX}/budget/users/{user_id}/accounts/',
])
@pytest.mark.parametrize('auth_headers, user_id, status_code, response_detail', [
    [lazy_fixture('auth_headers_ordinary_user'), 1, 403, "You don't have permission to do this"],
    [('Authorization', "Bearer"), 1, 401, "Could not validate credentials"],
    [lazy_fixture('auth_headers_ordinary_user'), 2, 200, None],
    [lazy_fixture('auth_headers_superuser'), 2, 200, None]
])
async def test_get_by_user_auth(
        auth_headers: tuple[Literal["Authorization"], str],
        url: str,
        status_code: int,
        response_detail: str,
        user_id: int,
        client: AsyncClient
):
    response = await client.get(
        url.format(DEFAULT_API_PREFIX=DEFAULT_API_PREFIX, user_id=user_id),
        headers=[auth_headers]
    )
    assert response.status_code == status_code
    if response.status_code != 200:
        assert response.json()['detail'] == response_detail


@pytest.mark.parametrize('url', [
    '{DEFAULT_API_PREFIX}/budget/accounts/{account_id}/',
    '{DEFAULT_API_PREFIX}/budget/accounts/{account_id}/incomes/'
])
@pytest.mark.parametrize(
    'auth_headers, account_id, status_code, response_detail', [
        [lazy_fixture('auth_headers_ordinary_user'), 1, 403, "You don't have permission to do this"],
        [('Authorization', "Bearer"), 1, 401, "Could not validate credentials"],
        [lazy_fixture('auth_headers_ordinary_user'), 2, 200, None],
        [lazy_fixture('auth_headers_superuser'), 2, 200, None]
    ]
)
async def test_get_by_account_auth(
        auth_headers: tuple[Literal["Authorization"], str],
        url: str,
        account_id: int,
        status_code: int,
        response_detail: int,
        client: AsyncClient
):
    response = await client.get(
        url.format(DEFAULT_API_PREFIX=DEFAULT_API_PREFIX, account_id=account_id),
        headers=[auth_headers]
    )
    assert response.status_code == status_code
    if response.status_code != 200:
        assert response.json()['detail'] == response_detail


@pytest.mark.parametrize(
    'auth_headers, income_id, status_code, response_detail', [
        [lazy_fixture('auth_headers_ordinary_user'), 1, 403, "You don't have permission to do this"],
        [('Authorization', "Bearer"), 1, 401, "Could not validate credentials"],
        [lazy_fixture('auth_headers_ordinary_user'), 4, 200, None],
        [lazy_fixture('auth_headers_superuser'), 4, 200, None]
    ]
)
async def test_certain_income_auth(
        auth_headers: tuple[Literal["Authorization"], str],
        income_id: int,
        status_code: int,
        response_detail: str,
        client: AsyncClient
):
    response = await client.get(
        f"{DEFAULT_API_PREFIX}/budget/incomes/{income_id}/",
        headers=[auth_headers]
    )
    assert response.status_code == status_code
    if response_detail:
        assert response.json()['detail'] == response_detail

    response = await client.delete(
        f"{DEFAULT_API_PREFIX}/budget/incomes/{income_id}/",
        headers=[auth_headers]
    )
    assert response.status_code == status_code
    if response_detail:
        assert response.json()['detail'] == response_detail


@pytest.mark.parametrize('url, data', [
    (f'{DEFAULT_API_PREFIX}/budget/incomes/', {
        "name": "test_income",
        "currency": Currencies.USD,
        "replenishment_account_id": 2,
        "amount": 2.0
    }),
    (f'{DEFAULT_API_PREFIX}/budget/accounts/', {
        "name": "test_account",
        "type": AccountTypes.BANK_ACCOUNT,
        "currency": Currencies.USD
    })
])
@pytest.mark.parametrize(
    'auth_headers, user_id, status_code, response_detail', [
        [lazy_fixture('auth_headers_ordinary_user'), 1, 403, "You don't have permission to do this"],
        [('Authorization', "Bearer"), 1, 401, "Could not validate credentials"],
        [lazy_fixture('auth_headers_ordinary_user'), 2, 201, None],
        [lazy_fixture('auth_headers_superuser'), 2, 201, None]
    ]
)
async def test_create_auth(
        auth_headers: tuple,
        url: str,
        data: dict,
        user_id: int,
        status_code: int,
        response_detail: str,
        client: AsyncClient
):
    data['user_id'] = user_id
    response = await client.post(
        url,
        headers=[auth_headers],
        json=data
    )
    assert response.status_code == status_code
    if response_detail:
        assert response.json()['detail'] == response_detail

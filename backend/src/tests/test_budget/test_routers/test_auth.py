from typing import Literal

import pytest
from httpx import AsyncClient
from pytest_lazyfixture import lazy_fixture

from backend.src.budget.config import Currencies, AccountTypes, SpendingCategories, IncomeCategories
from backend.src.config import API_PREFIX_V1

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize('url', [
    '{DEFAULT_API_PREFIX}/budget/users/{user_id}/incomes/',
    '{DEFAULT_API_PREFIX}/budget/users/{user_id}/accounts/',
    '{DEFAULT_API_PREFIX}/budget/users/{user_id}/spendings/'
])
@pytest.mark.parametrize('auth_headers, user_id, status_code, response_detail', [
    [lazy_fixture('auth_headers_ordinary_user'), 1, 403, "You don't have permission to do this"],
    [('Authorization', "Bearer"), 1, 401, "Could not validate credentials"],
    [lazy_fixture('auth_headers_ordinary_user'), 2, 200, None],
    [lazy_fixture('auth_headers_superuser'), 2, 200, None]
])
async def test_certain_user_auth(
        auth_headers: tuple[Literal["Authorization"], str],
        url: str,
        status_code: int,
        response_detail: str,
        user_id: int,
        client: AsyncClient
):
    response = await client.get(
        url.format(DEFAULT_API_PREFIX=API_PREFIX_V1, user_id=user_id),
        headers=[auth_headers]
    )
    assert response.status_code == status_code
    if response.status_code != 200:
        assert response.json()['detail'] == response_detail


@pytest.mark.parametrize('url, data', [
    ('{DEFAULT_API_PREFIX}/budget/accounts/{account_id}/', {
        "is_active": True
    }),
    ('{DEFAULT_API_PREFIX}/budget/accounts/{account_id}/incomes/', None),
    ('{DEFAULT_API_PREFIX}/budget/accounts/{account_id}/spendings/', None)
])
@pytest.mark.parametrize(
    'auth_headers, account_id, status_code, response_detail', [
        [lazy_fixture('auth_headers_ordinary_user'), 1, 403, "You don't have permission to do this"],
        [('Authorization', "Bearer"), 1, 401, "Could not validate credentials"],
        [lazy_fixture('auth_headers_ordinary_user'), 2, 200, None],
        [lazy_fixture('auth_headers_superuser'), 2, 200, None]
    ]
)
async def test_certain_account_auth(
        auth_headers: tuple[Literal["Authorization"], str],
        url: str,
        data: dict,
        account_id: int,
        status_code: int,
        response_detail: int,
        client: AsyncClient
):
    response = await client.get(
        url.format(DEFAULT_API_PREFIX=API_PREFIX_V1, account_id=account_id),
        headers=[auth_headers]
    )
    assert response.status_code == status_code
    if response.status_code != 200:
        assert response.json()['detail'] == response_detail

    if data:
        response = await client.patch(
            url.format(DEFAULT_API_PREFIX=API_PREFIX_V1, account_id=account_id),
            headers=[auth_headers],
            json=data
        )
        assert response.status_code == status_code
        if response_detail:
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
        f"{API_PREFIX_V1}/budget/incomes/{income_id}/",
        headers=[auth_headers]
    )
    assert response.status_code == status_code
    if response_detail:
        assert response.json()['detail'] == response_detail

    income_data = {
        "amount": 1
    }
    response = await client.patch(
        f'{API_PREFIX_V1}/budget/incomes/{income_id}/',
        headers=[auth_headers],
        json=income_data
    )
    assert response.status_code == status_code
    if response_detail:
        assert response.json()['detail'] == response_detail

    response = await client.delete(
        f"{API_PREFIX_V1}/budget/incomes/{income_id}/",
        headers=[auth_headers]
    )
    assert response.status_code == status_code
    if response_detail:
        assert response.json()['detail'] == response_detail


@pytest.mark.parametrize(
    'auth_headers, spending_id, status_code, response_detail', [
        [lazy_fixture('auth_headers_ordinary_user'), 1, 403, "You don't have permission to do this"],
        [('Authorization', "Bearer"), 1, 401, "Could not validate credentials"],
        [lazy_fixture('auth_headers_ordinary_user'), 4, 200, None],
        [lazy_fixture('auth_headers_superuser'), 4, 200, None]
    ]
)
async def test_certain_spending_auth(
        auth_headers: tuple[Literal["Authorization"], str],
        spending_id: int,
        status_code: int,
        response_detail: str,
        client: AsyncClient
):
    response = await client.get(
        f"{API_PREFIX_V1}/budget/spendings/{spending_id}/",
        headers=[auth_headers]
    )
    assert response.status_code == status_code
    if response_detail:
        assert response.json()['detail'] == response_detail

    spending_data = {
        "amount": 2
    }
    response = await client.patch(
        f'{API_PREFIX_V1}/budget/spendings/{spending_id}/',
        headers=[auth_headers],
        json=spending_data
    )
    assert response.status_code == status_code
    if response_detail:
        assert response.json()['detail'] == response_detail

    response = await client.delete(
        f"{API_PREFIX_V1}/budget/spendings/{spending_id}/",
        headers=[auth_headers]
    )
    assert response.status_code == status_code
    if response_detail:
        assert response.json()['detail'] == response_detail


@pytest.mark.parametrize('url, data', [
    (f'{API_PREFIX_V1}/budget/incomes/', {
        "comment": "test_income",
        "currency": Currencies.USD,
        "replenishment_account_id": 2,
        "amount": 2.0,
        "category": IncomeCategories.OTHER
    }),
    (f'{API_PREFIX_V1}/budget/accounts/', {
        "name": "test_account",
        "type": AccountTypes.BANK_ACCOUNT,
        "currency": Currencies.USD,
        "balance": 0
    }),
    (f'{API_PREFIX_V1}/budget/spendings/', {
        "name": "test_account",
        "currency": Currencies.USD,
        "receipt_account_id": 2,
        "amount": 2.0,
        "category": SpendingCategories.TAXI
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

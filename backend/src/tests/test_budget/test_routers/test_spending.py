import datetime
from typing import Literal

import pytest
from httpx import AsyncClient

from backend.src.budget.config import Currencies, SpendingCategories
from backend.src.budget.exceptions import AccountNotFoundException
from backend.src.budget.models import Spending
from backend.src.config import DEFAULT_API_PREFIX
from backend.src.tests.conftest import PRELOAD_DATA

pytestmark = pytest.mark.asyncio


async def test_get_all_spendings_with_suitable_query(
        client: AsyncClient,
        auth_headers_superuser: tuple[Literal["Authorization"], str]
):
    query_params = [('currency', Currencies.USD),
                    ('category', SpendingCategories.TAXI)]
    response = await client.get(
        f'{DEFAULT_API_PREFIX}/budget/users/1/spendings/',
        params=query_params,
        headers=[auth_headers_superuser]
    )
    print(response.json())
    assert response.status_code == 200
    response_spendings = response.json()

    preloaded_spendings = [
        PRELOAD_DATA[name]["data"] for name in PRELOAD_DATA
        if PRELOAD_DATA[name]["model"] == Spending
        and PRELOAD_DATA[name]["data"]["user_id"] == 1
        and PRELOAD_DATA[name]["data"]["currency"] == Currencies.USD
        and PRELOAD_DATA[name]["data"]["category"] == SpendingCategories.TAXI
    ]
    preloaded_spendings.reverse()

    assert len(response_spendings) == len(preloaded_spendings)

    for key, value in preloaded_spendings[0].items():
        if key != "receipt_account_id":
            assert response_spendings[0][key] == value
    assert response_spendings[0]['receipt_account']['id'] == preloaded_spendings[0]['receipt_account_id']


@pytest.mark.parametrize(
    "url", [
        f'{DEFAULT_API_PREFIX}/budget/users/1/spendings/',
        f'{DEFAULT_API_PREFIX}/budget/accounts/1/spendings/'
    ]
)
@pytest.mark.parametrize(
    'query_params', [
        ([('currency', Currencies.USD),
          ('created_at_ge', datetime.datetime.now()),
          ('created_at_le', datetime.datetime.now())]),
        ([('category', SpendingCategories.BILLS)]),
        ([('currency', Currencies.CNY)])
    ]
)
async def test_get_all_spendings_without_suitable_query(
        url: str,
        query_params: list[tuple],
        client: AsyncClient,
        auth_headers_superuser: tuple[Literal["Authorization"], str]
):
    query_params = [('currency', Currencies.USD),
                    ('created_at_ge', datetime.datetime.now()),
                    ('created_at_le', datetime.datetime.now())]

    response = await client.get(
        url=url,
        headers=[auth_headers_superuser],
        params=query_params
    )

    assert response.status_code == 200
    assert len(response.json()) == 0


@pytest.mark.parametrize(
    'url', [
        f'{DEFAULT_API_PREFIX}/budget/users/1/spendings/',
        f'{DEFAULT_API_PREFIX}/budget/accounts/1/spendings/'
    ]
)
@pytest.mark.parametrize(
    'query_params, status_code', [
        ([('created_at_ge', 'test_')], 422),
        ([('currency', 'test_')], 422),
        ([('created_at_le', 'test_')], 422),
        ([('currency', 'USA')], 422),
        ([('category', 'TEST')], 422)
    ]
)
async def test_all_spendings_wrong_query(
        url: str,
        query_params: list[tuple],
        status_code: int,
        client: AsyncClient,
        auth_headers_superuser: tuple[Literal["Authorization"], str]
):
    response = await client.get(
        url=url,
        headers=[auth_headers_superuser],
        params=query_params
    )
    assert response.status_code == status_code


@pytest.mark.parametrize('receipt_account_id', [1, 2])
async def test_get_all_spendings_by_account(
        receipt_account_id: int,
        client: AsyncClient,
        auth_headers_superuser: tuple[Literal["Authorization"], str]
):
    response = await client.get(
        f'{DEFAULT_API_PREFIX}/budget/accounts/{receipt_account_id}/spendings/',
        headers=[auth_headers_superuser]
    )

    assert response.status_code == 200

    preloaded_spendings = [
        PRELOAD_DATA[name]["data"] for name in PRELOAD_DATA
        if PRELOAD_DATA[name]["model"] == Spending
        and PRELOAD_DATA[name]["data"]['receipt_account_id'] == receipt_account_id
    ]
    response_spendings = response.json()

    assert len(response_spendings) == len(preloaded_spendings)
    for spending in response_spendings:
        assert spending['receipt_account_id'] == receipt_account_id


async def test_get_all_spending_nonexistent_account(
        auth_headers_superuser: tuple[Literal["Authorization"], str],
        client: AsyncClient
):
    response = await client.get(
        f"{DEFAULT_API_PREFIX}/budget/accounts/9999/spendings/",
        headers=[auth_headers_superuser]
    )
    assert response.status_code == 404
    assert response.json()['detail'] == AccountNotFoundException(9999).detail

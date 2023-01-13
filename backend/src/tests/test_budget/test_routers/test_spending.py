import datetime
from decimal import Decimal
from typing import Literal

import pytest
from httpx import AsyncClient

from backend.src.budget.config import Currencies, SpendingCategories
from backend.src.budget.exceptions import AccountNotFoundException, SpendingNotFoundException, \
    AccountNotBelongsToUserException, AccountNotExistsException, AccountBalanceWillGoNegativeException
from backend.src.budget.models import Spending, Account
from backend.src.config import DEFAULT_API_PREFIX
from backend.src.tests.conftest import PRELOAD_DATA
from backend.src.utils import convert_amount_to_another_currency

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
        assert spending['receipt_account']['id'] == receipt_account_id


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


@pytest.mark.parametrize('spending_id', [1, 2, 3])
async def test_get_certain_spending(
        spending_id: int,
        auth_headers_superuser: tuple[Literal["Authorization"], str],
        client: AsyncClient
):
    response = await client.get(
        f'{DEFAULT_API_PREFIX}/budget/spendings/{spending_id}/',
        headers=[auth_headers_superuser]
    )

    assert response.status_code == 200

    preloaded_spending = [
        PRELOAD_DATA[name]['data'] for name in PRELOAD_DATA
        if PRELOAD_DATA[name]['model'] == Spending
        and name.endswith(f'_{spending_id}')
    ][0]
    response_spending = response.json()

    for key, value in preloaded_spending.items():
        if key != 'receipt_account_id':
            assert response_spending[key] == value
    assert response_spending['receipt_account']['id'] == preloaded_spending['receipt_account_id']


async def test_get_nonexistent_income(
        client: AsyncClient,
        auth_headers_superuser: tuple[Literal["Authorization"], str]
):
    response = await client.get(
        f'{DEFAULT_API_PREFIX}/budget/spendings/9999/',
        headers=[auth_headers_superuser]
    )

    assert response.status_code == 404
    assert response.json()['detail'] == SpendingNotFoundException(9999).detail


@pytest.mark.parametrize('spending_data', [
    {
        "name": "test_spending",
        "user_id": 1,
        "currency": Currencies.USD,
        "receipt_account_id": 1,
        "amount": 2.3,
        "category": SpendingCategories.TAXI
    },
    {
        "name": "test_spending",
        "user_id": 2,
        "currency": Currencies.RUB,
        "receipt_account_id": 2,
        "amount": 60,
        "category": SpendingCategories.OTHER
    }
])
async def test_create_spending(
        spending_data: dict,
        auth_headers_superuser: tuple[Literal["Authorization"], str],
        client: AsyncClient
):
    response = await client.post(
        f'{DEFAULT_API_PREFIX}/budget/spendings/',
        headers=[auth_headers_superuser],
        json=spending_data
    )
    assert response.status_code == 201

    response_spending = response.json()

    for key, value in spending_data.items():
        if key != 'receipt_account_id':
            assert response_spending[key] == value
    assert response_spending['receipt_account']['id'] == spending_data['receipt_account_id']
    assert response_spending['amount_in_account_currency_at_creation'] == spending_data['amount']

    preloaded_account = [
        PRELOAD_DATA[name]['data'] for name in PRELOAD_DATA
        if PRELOAD_DATA[name]['model'] == Account
        and name.endswith(f'_{spending_data["receipt_account_id"]}')
    ][0]

    sum_of_spending_amount_and_preloaded_account_balance = \
        (preloaded_account['balance'] - Decimal(spending_data['amount'])).quantize(Decimal('.01'))
    response_account_balance = Decimal(response_spending['receipt_account']['balance']).quantize(Decimal('.01'))
    assert sum_of_spending_amount_and_preloaded_account_balance == response_account_balance


async def test_create_spending_with_different_currency_from_account(
        client: AsyncClient,
        auth_headers_superuser: tuple[Literal["Authorization"], str],
):
    spending_data = {
        "name": "test_spending",
        "user_id": 1,
        "currency": Currencies.CNY,
        "receipt_account_id": 1,
        "amount": 2.30,
        "category": SpendingCategories.TAXI
    }

    get_spending_response = await client.get(
        f'{DEFAULT_API_PREFIX}/budget/spendings/1/',
        headers=[auth_headers_superuser]
    )
    account_before_spending_creation = get_spending_response.json()['receipt_account']

    create_spending_response = await client.post(
        f'{DEFAULT_API_PREFIX}/budget/spendings/',
        headers=[auth_headers_superuser],
        json=spending_data
    )
    assert create_spending_response.status_code == 201

    spending_amount_in_account_currency = await convert_amount_to_another_currency(
        amount=spending_data['amount'],
        currency=spending_data['currency'],
        desired_currency=account_before_spending_creation['currency']
    )

    response_spending = create_spending_response.json()
    for key, value in spending_data.items():
        if key != 'receipt_account_id':
            assert response_spending[key] == value
    assert response_spending['receipt_account']['id'] == spending_data['receipt_account_id']
    assert Decimal(response_spending['amount_in_account_currency_at_creation']).quantize(Decimal('.01')) == \
        spending_amount_in_account_currency
    assert response_spending['receipt_account']['balance'] < account_before_spending_creation['balance']


@pytest.mark.parametrize('spending_data, status_code, detail', [
    ({
        "name": "test_spending",
        "user_id": 1,
        "currency": "dsdsafdsf",
        "receipt_account_id": 1,
        "amount": 2.30,
        "category": SpendingCategories.TAXI
    }, 422, None),
    ({
        "name": "test_spending",
        "user_id": 1,
        "currency": Currencies.USD,
        "receipt_account_id": 1,
        "amount": -2.30,
        "category": SpendingCategories.TAXI
    }, 422, None),
    ({
        "name": "test_spending",
        "user_id": 1,
        "currency": Currencies.USD,
        "receipt_account_id": 1,
        "amount": 2.30,
        "category": "djafjdfjsajf"
    }, 422, None),
    ({
        "name": "test_spending",
        "user_id": 1,
        "currency": Currencies.USD,
        "receipt_account_id": 1,
        "amount": 2.333333,
        "category": SpendingCategories.TAXI
    }, 422, None),
    ({
        "name": "test_spending",
        "user_id": 1,
        "currency": Currencies.USD,
        "receipt_account_id": 2,
        "amount": 2.30,
        "category": SpendingCategories.TAXI
    }, 400, AccountNotBelongsToUserException(2, 1).detail),
    ({
        "name": "test_spending",
        "user_id": 1,
        "currency": Currencies.USD,
        "receipt_account_id": 9999,
        "amount": 2.30,
        "category": SpendingCategories.TAXI
    }, 400, AccountNotExistsException(9999).detail),
    ({
        "name": "test_spending",
        "user_id": 999,
        "currency": Currencies.USD,
        "receipt_account_id": 1,
        "amount": 2.30,
        "category": SpendingCategories.TAXI
    }, 400, AccountNotBelongsToUserException(1, 999).detail),
    ({
        "name": "test_spending",
        "user_id": 1,
        "currency": Currencies.USD,
        "receipt_account_id": 1,
        "amount": 99999,
        "category": SpendingCategories.TAXI
    }, 400, AccountBalanceWillGoNegativeException().detail),
    ({}, 422, None)
])
async def test_create_incorrect_spending(
        spending_data: dict,
        status_code: int,
        detail: str,
        client: AsyncClient,
        auth_headers_superuser: tuple[Literal["Authorization"], str],
):
    response = await client.post(
        f'{DEFAULT_API_PREFIX}/budget/spendings/',
        headers=[auth_headers_superuser],
        json=spending_data
    )
    assert response.status_code == status_code
    if detail:
        assert response.json()['detail'] == detail

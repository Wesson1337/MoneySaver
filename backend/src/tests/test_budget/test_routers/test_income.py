import datetime
from decimal import Decimal
from typing import Literal

import pytest
from httpx import AsyncClient

from backend.src.budget.config import Currencies
from backend.src.budget.exceptions import IncomeNotFoundException, AccountNotFoundException, \
    AccountNotBelongsToUserException, AccountNotExistsException, \
    AccountBalanceWillGoNegativeException
from backend.src.budget.models import Income, Account
from backend.src.config import DEFAULT_API_PREFIX
from backend.src.tests.conftest import PRELOAD_DATA
from backend.src.utils import convert_amount_to_another_currency

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize('income_index', [0, 1])
async def test_get_all_incomes_with_suitable_query(
        income_index,
        client: AsyncClient,
        auth_headers_superuser: tuple[Literal["Authorization"], str]
):
    query_params = [('currency', Currencies.USD),
                    ('created_at_ge', datetime.datetime(year=2022, month=1, day=1)),
                    ('created_at_le', datetime.datetime.now())]
    response = await client.get(
        f'{DEFAULT_API_PREFIX}/budget/users/1/incomes/',
        params=query_params,
        headers=[auth_headers_superuser]
    )
    assert response.status_code == 200
    response_incomes = response.json()

    preloaded_incomes_with_us_currency = [
        PRELOAD_DATA[name]['data'] for name in PRELOAD_DATA
        if PRELOAD_DATA[name]['model'] == Income
        and PRELOAD_DATA[name]['data']['user_id'] == 1
        and PRELOAD_DATA[name]['data']['currency'] == Currencies.USD
    ]
    preloaded_incomes_with_us_currency.reverse()

    assert len(response.json()) == len(preloaded_incomes_with_us_currency)

    assert response_incomes[income_index]['currency'] == preloaded_incomes_with_us_currency[income_index]['currency']
    assert response_incomes[income_index]['replenishment_account']['id'] == \
           preloaded_incomes_with_us_currency[income_index]['replenishment_account_id']
    assert response_incomes[income_index]['amount'] == preloaded_incomes_with_us_currency[income_index]['amount']
    assert response_incomes[income_index]['amount_in_account_currency_at_creation'] == \
           preloaded_incomes_with_us_currency[income_index]['amount_in_account_currency_at_creation']


@pytest.mark.parametrize(
    'url', [
        f'{DEFAULT_API_PREFIX}/budget/users/1/incomes/',
        f'{DEFAULT_API_PREFIX}/budget/accounts/1/incomes/'
    ]
)
@pytest.mark.parametrize(
    'query_params', [
        (
                [('currency', Currencies.USD),
                 ('created_at_ge', datetime.datetime.now()),
                 ('created_at_le', datetime.datetime.now())]
        ),
        (
                [('currency', Currencies.CNY)]
        )
    ]
)
async def test_get_all_incomes_without_suitable_query(
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
        f'{DEFAULT_API_PREFIX}/budget/users/1/incomes/',
        f'{DEFAULT_API_PREFIX}/budget/accounts/1/incomes/'
    ]
)
@pytest.mark.parametrize(
    'query_params, status_code', [
        ([('created_at_ge', 'test_')], 422),
        ([('currency', 'test_')], 422),
        ([('created_at_le', 'test_')], 422),
        ([('currency', 'USA')], 422),
    ]
)
async def test_get_all_incomes_with_wrong_query(
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


@pytest.mark.parametrize('replenishment_account_id', [1, 2])
async def test_get_all_incomes_by_account(
        replenishment_account_id: int,
        client: AsyncClient,
        auth_headers_superuser: tuple[Literal["Authorization"], str]
):
    response = await client.get(
        f'{DEFAULT_API_PREFIX}/budget/accounts/{replenishment_account_id}/incomes/',
        headers=[auth_headers_superuser]
    )

    assert response.status_code == 200

    preloaded_incomes = [
        PRELOAD_DATA[name]['data'] for name in PRELOAD_DATA
        if PRELOAD_DATA[name]['model'] == Income
        and PRELOAD_DATA[name]['data']['replenishment_account_id'] == replenishment_account_id
    ]
    response_incomes = response.json()

    assert len(response_incomes) == len(preloaded_incomes)
    for income in response_incomes:
        assert income['replenishment_account']['id'] == replenishment_account_id


async def test_get_all_incomes_by_account_nonexistent_account(
        auth_headers_superuser: tuple[Literal["Authorization"], str],
        client: AsyncClient
):
    response = await client.get(
        f"{DEFAULT_API_PREFIX}/budget/accounts/9999/incomes/",
        headers=[auth_headers_superuser]
    )
    assert response.status_code == 404
    assert response.json()['detail'] == AccountNotFoundException(9999).detail


@pytest.mark.parametrize('income_id', [1, 2, 3])
async def test_get_certain_income(
        income_id: int,
        auth_headers_superuser: tuple[Literal["Authorization"], str],
        client: AsyncClient
):
    response = await client.get(
        f'{DEFAULT_API_PREFIX}/budget/incomes/{income_id}/',
        headers=[auth_headers_superuser]
    )

    assert response.status_code == 200

    preloaded_income = [
        PRELOAD_DATA[name]['data'] for name in PRELOAD_DATA
        if PRELOAD_DATA[name]['model'] == Income
        and name.endswith(f'_{income_id}')
    ]

    response_income = response.json()

    assert preloaded_income[0]['name'] == response_income['name']
    assert preloaded_income[0]['amount'] == response_income['amount']
    assert preloaded_income[0]['currency'] == response_income['currency']


async def test_get_nonexistent_income(
        client: AsyncClient,
        auth_headers_superuser: tuple[Literal["Authorization"], str]
):
    response = await client.get(
        f'{DEFAULT_API_PREFIX}/budget/incomes/9999/',
        headers=[auth_headers_superuser]
    )

    assert response.status_code == 404
    assert response.json() == {'detail': IncomeNotFoundException(9999).detail}


@pytest.mark.parametrize('income_data', [
    {
        "name": "test_income",
        "user_id": 1,
        "currency": Currencies.USD,
        "replenishment_account_id": 1,
        "amount": 2.30
    },
    {
        "name": "test_income",
        "user_id": 2,
        "currency": Currencies.RUB,
        "replenishment_account_id": 2,
        "amount": 200
    }
])
async def test_create_income(
        income_data: dict,
        auth_headers_superuser: tuple[Literal["Authorization"], str],
        client: AsyncClient
):
    response = await client.post(
        f'{DEFAULT_API_PREFIX}/budget/incomes/',
        headers=[auth_headers_superuser],
        json=income_data
    )
    assert response.status_code == 201

    income_json = response.json()

    assert income_json['name'] == income_data['name']
    assert income_json['currency'] == income_data['currency']
    assert income_json['replenishment_account']['id'] == income_data['replenishment_account_id']
    assert income_json['amount'] == income_data['amount']
    assert income_json['amount_in_account_currency_at_creation'] == \
           income_data['amount']

    preloaded_account = [
        PRELOAD_DATA[name]['data'] for name in PRELOAD_DATA
        if PRELOAD_DATA[name]['model'] == Account
        and name.endswith(f'_{income_data["replenishment_account_id"]}')
    ][0]

    preloaded_account_balance = preloaded_account['balance']
    sum_of_income_amount_and_preload_account_balance = \
        preloaded_account_balance.quantize(Decimal('.01')) + Decimal(income_data['amount']).quantize(Decimal('.01'))
    response_account_balance = Decimal(income_json['replenishment_account']['balance']).quantize(Decimal('.01'))
    assert response_account_balance == sum_of_income_amount_and_preload_account_balance


async def test_create_income_with_different_currency_from_account(
        client: AsyncClient,
        auth_headers_superuser: tuple[Literal["Authorization"], str],
):
    income_data = {
        "name": "test_income",
        "user_id": 1,
        "currency": "CNY",
        "replenishment_account_id": 1,
        "amount": 2.30
    }

    get_income_response = await client.get(
        f'{DEFAULT_API_PREFIX}/budget/incomes/1/',
        headers=[auth_headers_superuser]
    )
    replenishment_account_before_income_creation = get_income_response.json()['replenishment_account']

    create_income_response = await client.post(
        f'{DEFAULT_API_PREFIX}/budget/incomes/',
        headers=[auth_headers_superuser],
        json=income_data
    )

    income_amount_in_account_currency = await convert_amount_to_another_currency(
        amount=income_data['amount'],
        currency=income_data['currency'],
        desired_currency=replenishment_account_before_income_creation['currency']
    )

    assert create_income_response.status_code == 201

    income_json = create_income_response.json()

    assert income_json['name'] == income_data['name']
    assert income_json['currency'] == income_data['currency']
    assert income_json['replenishment_account']['id'] == income_data['replenishment_account_id']
    assert income_json['amount'] == income_data['amount']
    assert Decimal(income_json['amount_in_account_currency_at_creation']).quantize(Decimal('.01')) == \
           income_amount_in_account_currency

    assert income_json['replenishment_account']['balance'] > replenishment_account_before_income_creation['balance']


@pytest.mark.parametrize('income_data, status_code, detail', [
    ({
         "name": "test_income",
         "user_id": 1,
         "currency": "dffjdjj",
         "replenishment_account_id": 1,
         "amount": 2.30
     }, 422, None),
    ({
         "name": "test_income",
         "currency": Currencies.RUB,
         "replenishment_account_id": 2,
         "amount": 200
     }, 422, None),
    ({
         "name": "test_income",
         "user_id": 1,
         "currency": "USD",
         "replenishment_account_id": 1,
         "amount": 2.3333
     }, 422, None),
    ({
         "name": "test_income",
         "user_id": 1,
         "currency": "USD",
         "replenishment_account_id": 2,
         "amount": 2.33
     }, 400, AccountNotBelongsToUserException(2, 1).detail),
    ({
         "name": "test_income",
         "user_id": 1,
         "currency": "USD",
         "replenishment_account_id": 999,
         "amount": 2.33
     }, 400, AccountNotExistsException(999).detail),
    ({
         "name": "test_income",
         "user_id": 999,
         "currency": "USD",
         "replenishment_account_id": 1,
         "amount": 2.33
     }, 400, AccountNotBelongsToUserException(1, 999).detail),
    ({}, 422, None)
])
async def test_create_incorrect_income(
        income_data: dict,
        status_code: int,
        detail: str,
        client: AsyncClient,
        auth_headers_superuser: tuple[Literal["Authorization"], str],
):
    response = await client.post(
        f'{DEFAULT_API_PREFIX}/budget/incomes/',
        headers=[auth_headers_superuser],
        json=income_data
    )
    assert response.status_code == status_code
    if detail:
        assert response.json()['detail'] == detail


async def test_income_patch(
        auth_headers_superuser: tuple[Literal["Authorization"], str],
        client: AsyncClient
):
    income_data = {
        "name": "test_income",
        "amount": 0.9
    }
    get_income_response = await client.get(
        f'{DEFAULT_API_PREFIX}/budget/incomes/1/',
        headers=[auth_headers_superuser]
    )
    replenishment_account_before_income_patch = get_income_response.json()['replenishment_account']
    income_amount_before_patch = get_income_response.json()['amount']

    response = await client.patch(
        f'{DEFAULT_API_PREFIX}/budget/incomes/1/',
        json=income_data,
        headers=[auth_headers_superuser]
    )

    assert response.status_code == 200

    income_json = response.json()
    assert income_json['name'] == income_data['name']
    assert income_json['amount'] == income_data['amount']
    assert income_json['amount_in_account_currency_at_creation'] == \
           income_data['amount']

    new_and_old_income_amount_difference = Decimal(income_data['amount']) - Decimal(income_amount_before_patch)
    assert Decimal(income_json['replenishment_account']['balance']).quantize(Decimal('.01')) == \
           Decimal(replenishment_account_before_income_patch['balance']).quantize(Decimal('.01')) + \
           new_and_old_income_amount_difference.quantize(Decimal('.01'))


@pytest.mark.parametrize(
    'income_data', [
        {
            "name": "test_income",
            "amount": 60
        },
        {
            "name": "test",
            "amount": 1
        }
    ]
)
async def test_income_patch_with_different_currency_from_account(
        income_data: dict,
        auth_headers_superuser: tuple[Literal["Authorization"], str],
        client: AsyncClient
):

    get_income_response = await client.get(
        f'{DEFAULT_API_PREFIX}/budget/incomes/2/',
        headers=[auth_headers_superuser]
    )
    stored_income = get_income_response.json()
    replenishment_account_before_income_patch = stored_income['replenishment_account']

    incomes_difference_in_account_currency = await convert_amount_to_another_currency(
        amount=Decimal(income_data['amount'] - stored_income['amount']),
        currency=stored_income['currency'],
        desired_currency=replenishment_account_before_income_patch['currency'],
    )

    response = await client.patch(
        f'{DEFAULT_API_PREFIX}/budget/incomes/2/',
        headers=[auth_headers_superuser],
        json=income_data
    )

    assert response.status_code == 200

    income_json = response.json()
    assert income_json['name'] == income_data['name']
    assert income_json['amount'] == income_data['amount']
    assert stored_income['amount'] != income_json['amount']
    assert Decimal(income_json['amount_in_account_currency_at_creation']).quantize(Decimal('.01')) == \
        Decimal(stored_income['amount_in_account_currency_at_creation']).quantize(Decimal('.01')) + \
        incomes_difference_in_account_currency

    assert Decimal(income_json['replenishment_account']['balance']) != \
           Decimal(replenishment_account_before_income_patch['balance'])


@pytest.mark.parametrize("income_data, status_code", [
    ({"amount": 1.222}, 422),
    ({"amount": -1}, 422),
    ({}, 400)
])
async def test_income_patch_with_incorrect_data(
        income_data: dict,
        status_code: int,
        auth_headers_superuser: tuple[Literal["Authorization"], str],
        client: AsyncClient
):
    response = await client.patch(
        f'{DEFAULT_API_PREFIX}/budget/incomes/1/',
        headers=[auth_headers_superuser],
        json=income_data
    )
    assert response.status_code == status_code


async def test_patch_nonexistent_income(
        auth_headers_superuser: tuple[Literal["Authorization"], str],
        client: AsyncClient
):
    response = await client.patch(
        f'{DEFAULT_API_PREFIX}/budget/incomes/9999/',
        headers=[auth_headers_superuser],
        json={}
    )
    assert response.status_code == 404
    assert response.json()['detail'] == IncomeNotFoundException(9999).detail


async def test_income_delete(
        auth_headers_superuser: tuple[Literal["Authorization"], str],
        client: AsyncClient
):
    get_income_response = await client.get(
        f'{DEFAULT_API_PREFIX}/budget/incomes/2/',
        headers=[auth_headers_superuser]
    )
    stored_income = get_income_response.json()

    delete_response = await client.delete(
        f'{DEFAULT_API_PREFIX}/budget/incomes/2/',
        headers=[auth_headers_superuser]
    )
    assert delete_response.status_code == 200
    assert delete_response.json() == {'message': 'success'}

    deleted_income_get_response = await client.get(
        f'{DEFAULT_API_PREFIX}/budget/incomes/2/',
        headers=[auth_headers_superuser]
    )
    assert deleted_income_get_response.status_code == 404

    get_second_income_response = await client.get(
        f'{DEFAULT_API_PREFIX}/budget/incomes/1/',
        headers=[auth_headers_superuser]
    )
    updated_account = get_second_income_response.json()['replenishment_account']

    assert Decimal(stored_income['replenishment_account']['balance']).quantize(Decimal('.01')) == \
           Decimal(updated_account['balance']).quantize(Decimal('.01')) + \
           Decimal(stored_income['amount_in_account_currency_at_creation']).quantize(Decimal('.01'))


async def test_delete_nonexistent_income(
        client: AsyncClient,
        auth_headers_superuser: tuple[Literal["Authorization"], str],
):
    all_incomes_response_before_deletion = await client.get(
        f'{DEFAULT_API_PREFIX}/budget/incomes/',
        headers=[auth_headers_superuser]
    )

    response = await client.delete(
        f'{DEFAULT_API_PREFIX}/budget/incomes/999/',
        headers=[auth_headers_superuser]
    )
    assert response.status_code == 404

    all_incomes_response_after_deletion = await client.get(
        f'{DEFAULT_API_PREFIX}/budget/incomes/',
        headers=[auth_headers_superuser]
    )
    assert all_incomes_response_before_deletion.json() == all_incomes_response_after_deletion.json()


async def test_income_delete_with_greater_amount_than_account_balance(
        auth_headers_superuser: tuple[Literal["Authorization"], str],
        client: AsyncClient
):
    response = await client.delete(
        f'{DEFAULT_API_PREFIX}/budget/incomes/3/',
        headers=[auth_headers_superuser]
    )
    assert response.status_code == 400
    assert response.json()['detail'] == AccountBalanceWillGoNegativeException().detail


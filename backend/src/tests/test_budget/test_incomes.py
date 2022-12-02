import datetime
from decimal import Decimal

import pytest
from httpx import AsyncClient

from backend.src.budget.exceptions import IncomeNotFoundException
from backend.src.budget.models import Income, Account
from backend.src.config import Currencies
from backend.src.tests.conftest import PRELOAD_DATA

pytestmark = pytest.mark.asyncio


async def test_get_all_incomes(client: AsyncClient):
    response = await client.get('/api/v1/budget/incomes/')
    assert response.status_code == 200

    response_incomes = response.json()

    preloaded_incomes = tuple((entity for entity in PRELOAD_DATA if entity['model'] == Income))

    assert len(response_incomes) == len(preloaded_incomes)

    assert response_incomes[0].get('currency') == Currencies.RUB
    assert response_incomes[0].get('amount') == Decimal(1.5)
    assert response_incomes[0].get('replenishment_account').get('id') == 1


async def test_get_all_incomes_with_suitable_query(client: AsyncClient):
    query_params = [('currency', Currencies.USD),
                    ('created_at_ge', datetime.datetime(year=2022, month=1, day=1)),
                    ('created_at_le', datetime.datetime.now())]
    response = await client.get('/api/v1/budget/incomes/', params=query_params)

    print(response.json())

    assert response.status_code == 200

    response_incomes = response.json()

    preloaded_incomes_with_us_currency = tuple(
        (entity for entity in PRELOAD_DATA if entity['model'] == Income
         and entity['data']['currency'] == Currencies.USD)
    )

    assert len(response.json()) == len(preloaded_incomes_with_us_currency)

    assert response_incomes[0]['currency'] == preloaded_incomes_with_us_currency[0]['data']['currency']
    assert response_incomes[0]['replenishment_account']['id'] == \
           preloaded_incomes_with_us_currency[0]['data']['replenishment_account_id']
    assert response_incomes[0]['amount'] == preloaded_incomes_with_us_currency[0]['data']['amount']


async def test_get_all_incomes_without_suitable_query(client: AsyncClient):
    query_params = [('currency', Currencies.USD),
                    ('created_at_ge', datetime.datetime.now()),
                    ('created_at_le', datetime.datetime.now())]

    response = await client.get('/api/v1/budget/incomes/', params=query_params)

    assert response.status_code == 200
    assert len(response.json()) == 0


async def test_get_all_incomes_with_wrong_query(client: AsyncClient):
    query_params = [('currency', 'test_'),
                    ('created_at_ge', 'test'),
                    ('test', 'test')]
    response = await client.get('/api/v1/budget/incomes/', params=query_params)
    assert response.status_code == 422


async def test_get_all_incomes_by_account(client: AsyncClient):
    response = await client.get('/api/v1/budget/accounts/1/incomes/')

    assert response.status_code == 200

    response_incomes = response.json()

    assert len(response_incomes) == 2
    for income in response_incomes:
        assert income['replenishment_account']['id'] == 1


async def test_get_certain_income(client: AsyncClient):
    response = await client.get('/api/v1/budget/incomes/1/')

    assert response.status_code == 200

    preload_income = tuple((entity for entity in PRELOAD_DATA if entity['model'] == Income))[0]

    response_income = response.json()

    assert preload_income['data']['name'] == response_income['name']
    assert preload_income['data']['amount'] == response_income['amount']
    assert preload_income['data']['currency'] == response_income['currency']


async def test_get_nonexistent_income(client: AsyncClient):
    response = await client.get('/api/v1/budget/incomes/9999/')

    assert response.status_code == 404
    assert response.json() == {'detail': IncomeNotFoundException().detail}


async def test_create_income(client: AsyncClient):
    income_data = {
        "name": "test_income",
        "currency": "USD",
        "replenishment_account_id": 1,
        "amount": 2.30
    }

    response = await client.post('/api/v1/budget/incomes/', json=income_data)

    assert response.status_code == 201

    income_json = response.json()
    preloaded_account = tuple((entity for entity in PRELOAD_DATA if entity['model'] == Account))[0]

    assert income_json['name'] == income_data['name']
    assert income_json['currency'] == income_data['currency']
    assert income_json['replenishment_account']['id'] == income_data['replenishment_account_id']
    assert income_json['amount'] == income_data['amount']

    preloaded_account_balance = preloaded_account['data']['balance']
    sum_of_income_amount_and_preload_account_balance = \
        preloaded_account_balance.quantize(Decimal('.01')) + Decimal(income_data['amount']).quantize(Decimal('.01'))
    response_account_balance = Decimal(income_json['replenishment_account']['balance']).quantize(Decimal('.01'))
    assert response_account_balance == sum_of_income_amount_and_preload_account_balance


async def test_create_incorrect_income(client: AsyncClient):
    income_data = {
        "name": "test_income",
        "currency": "dffjdjj",
        "replenishment_account_id": 1,
        "amount": 2.30
    }
    response = await client.post('/api/v1/budget/incomes/', json=income_data)
    assert response.status_code == 422

    income_data = {
        "name": "test_income",
        "currency": "USD",
        "replenishment_account_id": 1,
        "amount": 2.3333
    }
    response = await client.post('/api/v1/budget/incomes/', json=income_data)
    assert response.status_code == 422

    income_data = {
        "name": "test_income",
        "currency": "USD",
        "replenishment_account_id": 3,
        "amount": 2.33
    }
    response = await client.post('/api/v1/budget/incomes/', json=income_data)
    assert response.status_code == 400

    income_data = {}
    response = await client.post('/api/v1/budget/incomes/', json=income_data)
    assert response.status_code == 422


async def test_income_patch():
    pass
    # TODO add this test

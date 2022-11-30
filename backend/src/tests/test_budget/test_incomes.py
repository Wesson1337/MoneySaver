import datetime
from decimal import Decimal

import pytest
from httpx import AsyncClient

from backend.src.budget.models import Income
from backend.src.tests.conftest import PRELOAD_DATA

pytestmark = pytest.mark.asyncio


async def test_get_all_incomes(client: AsyncClient):
    response = await client.get('/api/budget/incomes/')
    assert response.status_code == 200

    response_incomes = response.json()

    preloaded_incomes = tuple((table for table in PRELOAD_DATA if table['table_name'] == Income))

    assert len(response_incomes) == len(preloaded_incomes)

    assert response_incomes[0].get('currency') == 'RUB'
    assert response_incomes[0].get('amount') == Decimal(1.5)
    assert response_incomes[0].get('replenishment_account').get('id') == 1


async def test_get_all_incomes_with_suitable_query(client: AsyncClient):
    query_params = [('currency', 'US'),
                    ('created_at_ge', datetime.datetime(year=2022, month=1, day=1)),
                    ('created_at_le', datetime.datetime.now())]
    response = await client.get('/api/budget/incomes/', params=query_params)

    assert response.status_code == 200

    response_incomes = response.json()

    preloaded_incomes_with_us_currency = tuple(
        (table for table in PRELOAD_DATA if table['table_name'] == Income and table['data']['currency'] == 'US')
    )

    assert len(response.json()) == len(preloaded_incomes_with_us_currency)

    assert response_incomes[0]['currency'] == preloaded_incomes_with_us_currency[0]['data']['currency']
    assert response_incomes[0]['replenishment_account']['id'] == \
           preloaded_incomes_with_us_currency[0]['data']['replenishment_account_id']
    assert response_incomes[0]['amount'] == preloaded_incomes_with_us_currency[0]['data']['amount']


async def test_get_all_incomes_without_suitable_query(client: AsyncClient):
    query_params = [('currency', 'US'),
                    ('created_at_ge', datetime.datetime.now()),
                    ('created_at_le', datetime.datetime.now())]

    response = await client.get('/api/budget/incomes/', params=query_params)

    assert response.status_code == 200
    assert len(response.json()) == 0


async def test_get_all_incomes_with_wrong_query(client: AsyncClient):
    query_params = ['currency', 'test_',
                    ('created_at_ge', 'test')]

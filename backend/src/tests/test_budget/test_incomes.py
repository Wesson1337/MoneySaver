from decimal import Decimal

import pytest
from httpx import AsyncClient

from backend.src.budget.models import Income
from backend.src.tests.conftest import PRELOAD_DATA

pytestmark = pytest.mark.asyncio


async def test_get_all_incomes(client: AsyncClient):
    response = await client.get('/api/budget/incomes/')
    assert response.status_code == 200

    incomes = response.json()

    preloaded_incomes = tuple(filter(lambda table: table["table_name"] == Income, PRELOAD_DATA))

    assert len(incomes) == len(preloaded_incomes)

    assert incomes[-1].get('currency') == 'US'
    assert incomes[-1].get('amount') == Decimal(1.4)
    assert incomes[-1].get('replenishment_account').get('type') == 'BANK_ACCOUNT'

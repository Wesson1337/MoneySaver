from decimal import Decimal

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_get_all_incomes(client: AsyncClient):
    response = await client.get('/api/budget/incomes/')
    assert response.status_code == 200

    incomes = response.json()

    assert len(incomes) == 1

    assert incomes[-1].get('currency') == 'US'
    assert incomes[-1].get('amount') == Decimal(1.4)
    assert incomes[-1].get('replenishment_account').get('type') == 'BANK_ACCOUNT'

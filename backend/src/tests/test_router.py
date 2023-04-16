from _decimal import Decimal
from typing import Literal

import pytest
from aioredis import Redis
from httpx import AsyncClient

from backend.src.budget.config import Currencies
from backend.src.config import API_PREFIX_V1
from backend.src.utils import get_current_exchange_rate

pytestmark = pytest.mark.asyncio


async def test_get_exchange_rate_with_supported_currencies(
        redis: Redis,
        auth_headers_superuser: tuple[Literal["Authorization"], str],
        client: AsyncClient
):
    supported_currencies = [field.value for field in Currencies]
    for currency in supported_currencies:
        query_params = [("base_currency", Currencies.RUB), ("desired_currency", currency)]
        response = await client.get(
            f'{API_PREFIX_V1}/currency/',
            headers=[auth_headers_superuser],
            params=query_params
        )
        assert response.status_code == 200
        assert Decimal(response.text) == await get_current_exchange_rate(Currencies.RUB, currency, redis)


@pytest.mark.parametrize("query_params, status_code", [
    ([("base_currency", Currencies.RUB), ("desired_currency", "fdjkajfk")], 422),
    ([("desired_currency", Currencies.RUB)], 422),
    ([("base_currency", "fdjsjfddjf"), ("desired_currency", Currencies.USD)], 422),
    ([("base_currency", Currencies.RUB)], 422),
    ([], 422),
])
async def test_get_exchange_rate_with_unsupported_currencies(
        auth_headers_superuser: tuple[Literal["Authorization"], str],
        client: AsyncClient,
        query_params: list[tuple[str, Currencies]],
        status_code: int
):
    response = await client.get(
        f'{API_PREFIX_V1}/currency/',
        headers=[auth_headers_superuser],
        params=query_params
    )
    assert response.status_code == status_code

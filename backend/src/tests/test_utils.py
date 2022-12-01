from decimal import Decimal

import pytest

from backend.src.config import Currencies
from backend.src.utils.service import convert_amount_to_another_currency

pytestmark = pytest.mark.asyncio


async def test_convert_amount_to_another_currency():
    amount_in_usd = Decimal(5.0)
    amount_in_rub = await convert_amount_to_another_currency(amount_in_usd, Currencies.USD, Currencies.RUB)

    assert amount_in_rub > amount_in_usd

    new_amount_in_usd = await convert_amount_to_another_currency(amount_in_rub, Currencies.RUB, Currencies.USD)

    assert amount_in_rub > new_amount_in_usd
    assert amount_in_usd == new_amount_in_usd

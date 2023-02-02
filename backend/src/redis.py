import json
from typing import Type, Optional

import aioredis
import sqlalchemy
from aioredis import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from backend.src import config
from backend.src.auth.models import User
from backend.src.auth.schemas import UserSchemaOut
from backend.src.budget.models import Income, Account, Spending
from backend.src.budget.schemas.account import AccountSchemaOut
from backend.src.budget.schemas.income import IncomeSchemaOut
from backend.src.budget.schemas.spending import SpendingSchemaOut
from backend.src.database import Base


async def init_redis_pool():
    redis = aioredis.from_url(config.REDIS_URL, password=config.REDIS_PASSWORD, decode_responses=True)
    yield redis
    await redis.close()


def prefixed_key(f):
    """
    A method decorator that prefixes return values.
    Prefixes any string that the decorated method `f` returns with the value of
    the `prefix` attribute on the owner object `self`.
    """

    def prefixed_method(*args, **kwargs):
        self = args[0]
        key = f(*args, **kwargs)
        if self.prefix:
            return f'{self.prefix}:{key}'
        else:
            return key

    return prefixed_method


class Keys:
    """Methods to generate key names for Redis data structures."""
    def __init__(self, prefix: Optional[str] = None, sql_model: Optional[Type[Base]] = None) -> object:
        self.prefix = prefix
        self.model = sql_model

    @prefixed_key
    def sql_model_key_by_id(self, model_id: int):
        return f"cache:{self.model.__tablename__}:{model_id}"


class RedisService:
    def __init__(self, redis: Redis):
        self._redis = redis

    async def set_cache(self, key: Keys, data: dict):
        await self._redis.set(
            key,
            json.dumps(data),
            ex=config.REDIS_CACHING_DURATION_SECONDS
        )

    async def get_cache(self, key: Keys):
        data = await self._redis.get(key)
        if data:
            parsed_data = json.loads(data)
            return json.loads(parsed_data)


async def seed_redis_from_db(session: AsyncSession, redis: Redis):
    config.logger.info('seeding redis from db..')
    service = RedisService(redis)
    cache_keys = await redis.keys('*')
    for key in cache_keys:
        await redis.delete(key)

    result = await session.execute(sqlalchemy.select(User))
    users = result.scalars().all()
    for user in users:
        key = Keys(sql_model=User).sql_model_key_by_id(user.id)
        await service.set_cache(key, UserSchemaOut.from_orm(user).json())

    result = await session.execute(sqlalchemy.select(Account))
    accounts = result.scalars().all()
    for account in accounts:
        key = Keys(sql_model=Account).sql_model_key_by_id(account.id)
        await service.set_cache(key, AccountSchemaOut.from_orm(account).json())

    result = await session.execute(sqlalchemy.select(Income).options(joinedload(Income.replenishment_account)))
    incomes = result.scalars().all()
    for income in incomes:
        key = Keys(sql_model=Income).sql_model_key_by_id(income.id)
        await service.set_cache(key, IncomeSchemaOut.from_orm(income).json())

    result = await session.execute(sqlalchemy.select(Spending).options(joinedload(Spending.receipt_account)))
    spendings = result.scalars().all()
    for spending in spendings:
        key = Keys(sql_model=Spending).sql_model_key_by_id(spending.id)
        await service.set_cache(key, SpendingSchemaOut.from_orm(spending).json())
    config.logger.info('seeding is done')

from dataclasses import dataclass
from typing import Protocol

import aioredis
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src import config
from backend.src.database import async_session


async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session


@dataclass
class BaseQueryParams(Protocol):
    pass


async def init_redis_pool():
    redis = aioredis.from_url(config.REDIS_URL, password=config.REDIS_PASSWORD, decode_responses=True)
    yield redis
    await redis.close()

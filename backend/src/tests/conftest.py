import asyncio
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Generator, Callable, Literal

import aioredis
import pytest_asyncio
from aioredis import Redis
from fastapi import FastAPI
from httpx import AsyncClient
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from backend.src import config
from backend.src.auth.config import JWT_SECRET_KEY, JWT_ALGORITHM
# noinspection PyUnresolvedReferences
from backend.src.auth.models import Base, User
from backend.src.budget.config import Currencies, AccountTypes, SpendingCategories
from backend.src.budget.models import Base, Account, Income, Spending
from backend.src.dependencies import get_async_session
from backend.src.main import app
from backend.src.redis import init_redis_pool, seed_redis_from_db

TEST_DATABASE_URL = "postgresql+asyncpg://" + config.TEST_DATABASE_URL

PRELOAD_DATA = {
    "user_1": {
        "model": User,
        "data": {
            "email": "testmail@example.com",
            # plain password = test_password
            "hashed_password": "$2b$12$Ql7XTNhMhDbIEHlYnBxQeOi1MMPS.yxx3cWt4j1FILtJ.VkMubnJy",
            "is_superuser": True,
            "is_active": True
        }
    },
    "user_2": {
        "model": User,
        "data": {
            "email": "test@example.com",
            # plain password = test_password
            "hashed_password": "$2b$12$kYRIvRY4vySCrR10hhZaVuRQCjU.78x2zaGpo2TsuSOjJVoVEBIyG",
            "is_superuser": False,
            "is_active": True
        }
    },
    "user_3": {
        "model": User,
        "data": {
            "email": "inactiveuser@example.com",
            # plain password = test_password
            "hashed_password": "$2b$12$kYRIvRY4vySCrR10hhZaVuRQCjU.78x2zaGpo2TsuSOjJVoVEBIyG",
            "is_superuser": False,
            "is_active": False
        }
    },
    "account_1": {
        "model": Account,
        "data": {
            "name": "test",
            "user_id": 1,
            "type": AccountTypes.BANK_ACCOUNT,
            "balance": Decimal(3),
            "currency": Currencies.USD,
            "is_active": True
        }
    },
    "account_2": {
        "model": Account,
        "data": {
            "name": "test",
            "user_id": 2,
            "type": AccountTypes.BANK_ACCOUNT,
            "balance": Decimal(1000),
            "currency": Currencies.RUB,
            "is_active": True
        }
    },
    "income_1": {
        "model": Income,
        "data": {
            "name": "test_income_1",
            "user_id": 1,
            "currency": Currencies.USD,
            "amount": Decimal(1.4),
            "replenishment_account_id": 1,
            "amount_in_account_currency_at_creation": Decimal(1.4)
        }
    },
    "income_2": {
        "model": Income,
        "data": {
            "name": "test_income_2",
            "user_id": 1,
            "currency": Currencies.RUB,
            "amount": Decimal(6),
            "replenishment_account_id": 1,
            "amount_in_account_currency_at_creation": Decimal(0.3)
        }
    },
    "income_3": {
        "model": Income,
        "data": {
            "name": "test_income_3",
            "user_id": 1,
            "currency": Currencies.USD,
            "amount": Decimal(2),
            "replenishment_account_id": 1,
            "amount_in_account_currency_at_creation": Decimal(9999)
        }
    },
    "income_4": {
        "model": Income,
        "data": {
            "name": "test_income_4",
            "user_id": 2,
            "currency": Currencies.RUB,
            "amount": Decimal(3.0),
            "replenishment_account_id": 2,
            "amount_in_account_currency_at_creation": Decimal(3.0)
        }
    },
    "spending_1": {
        "model": Spending,
        "data": {
            "name": "test_spending_1",
            "user_id": 1,
            "currency": Currencies.USD,
            "amount": Decimal(1.0),
            "receipt_account_id": 1,
            "amount_in_account_currency_at_creation": Decimal(3.0),
            "category": SpendingCategories.TAXI
        }
    },
    "spending_2": {
        "model": Spending,
        "data": {
            "name": "test_spending_2",
            "user_id": 2,
            "currency": Currencies.RUB,
            "amount": Decimal(1.0),
            "receipt_account_id": 2,
            "amount_in_account_currency_at_creation": Decimal(1.0),
            "category": SpendingCategories.OTHER
        }
    },
    "spending_3": {
        "model": Spending,
        "data": {
            "name": "test_spending_3",
            "user_id": 1,
            "currency": Currencies.RUB,
            "amount": Decimal(60.0),
            "receipt_account_id": 1,
            "amount_in_account_currency_at_creation": Decimal(1.0),
            "category": SpendingCategories.OTHER
        }
    },
    "spending_4": {
        "model": Spending,
        "data": {
            "name": "test_spending_4",
            "user_id": 2,
            "currency": Currencies.USD,
            "amount": Decimal(1.0),
            "receipt_account_id": 2,
            "amount_in_account_currency_at_creation": Decimal(60.0),
            "category": SpendingCategories.TAXI
        }
    }
}


@pytest_asyncio.fixture(scope="function")
def event_loop(request) -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_engine() -> AsyncEngine:
    engine = create_async_engine(TEST_DATABASE_URL)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def session(db_engine: AsyncEngine) -> AsyncSession:
    async_session = sessionmaker(bind=db_engine, expire_on_commit=False, class_=AsyncSession)
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        async with async_session(bind=conn) as session:
            yield session
            await session.rollback()


@pytest_asyncio.fixture(scope="function")
async def seed_db(session: AsyncSession) -> None:
    for entity in PRELOAD_DATA.values():
        session.add(entity["model"](**entity["data"]))
    await session.commit()


@pytest_asyncio.fixture(scope="function")
def override_get_async_session(session: AsyncSession) -> Callable:
    async def _override_get_async_session():
        yield session

    return _override_get_async_session


@pytest_asyncio.fixture(scope="function")
async def redis() -> Redis:
    redis = aioredis.from_url(config.TEST_REDIS_URL, password=config.TEST_REDIS_PASSWORD, decode_responses=True)
    yield redis
    keys = await redis.keys('*')
    await redis.close()


@pytest_asyncio.fixture(scope="function")
async def seed_test_redis_from_test_db(session: AsyncSession, redis: Redis):
    await seed_redis_from_db(session, redis)


@pytest_asyncio.fixture(scope="function")
def override_init_redis_pool(redis: Redis):
    async def _override_init_redis_pool():
        yield redis

    return _override_init_redis_pool


@pytest_asyncio.fixture(scope="function")
def test_app(override_get_async_session: Callable, override_init_redis_pool: Callable) -> FastAPI:
    app.dependency_overrides[get_async_session] = override_get_async_session
    app.dependency_overrides[init_redis_pool] = override_init_redis_pool
    return app


@pytest_asyncio.fixture(scope="function")
async def client(seed_db, test_app: FastAPI, seed_test_redis_from_test_db) -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        yield ac


@pytest_asyncio.fixture(scope="function")
async def superuser_encoded_jwt_token(seed_db, seed_test_redis_from_test_db) -> str:
    user_id = "1"
    data_to_encode = {"sub": user_id, "exp": datetime.utcnow() + timedelta(minutes=300)}
    encoded_jwt_token = jwt.encode(data_to_encode, JWT_SECRET_KEY, JWT_ALGORITHM)
    return encoded_jwt_token


@pytest_asyncio.fixture(scope="function")
async def auth_headers_superuser(superuser_encoded_jwt_token: str) -> tuple[Literal["Authorization"], str]:
    auth_headers = ('Authorization', f'Bearer {superuser_encoded_jwt_token}')
    return auth_headers


@pytest_asyncio.fixture(scope="function")
async def ordinary_user_encoded_jwt_token(seed_db, seed_test_redis_from_test_db) -> str:
    user_id = "2"
    data_to_encode = {"sub": user_id, "exp": datetime.utcnow() + timedelta(minutes=300)}
    encoded_jwt_token = jwt.encode(data_to_encode, JWT_SECRET_KEY, JWT_ALGORITHM)
    return encoded_jwt_token


@pytest_asyncio.fixture(scope="function")
async def auth_headers_ordinary_user(ordinary_user_encoded_jwt_token: str) -> tuple[Literal["Authorization"], str]:
    auth_headers = ('Authorization', f'Bearer {ordinary_user_encoded_jwt_token}')
    return auth_headers

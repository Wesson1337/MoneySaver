import asyncio
from decimal import Decimal
from typing import Generator, Callable

import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from backend.src.budget.models import Base, Account, Income
from backend.src.config import get_db_url
from backend.src.dependencies import get_async_session
from backend.src.main import app

TEST_DATABASE_URL = "postgresql+asyncpg://" + get_db_url(test=True)

PRELOAD_DATA = (
    {
        "model": Account,
        "data": {
            "name": 'test',
            "type": 'BANK_ACCOUNT',
            "balance": Decimal(1.23),
            "currency": "US"
        }
    },
    {
        "model": Income,
        "data": {
            "name": "test",
            "currency": "US",
            "amount": Decimal(1.4),
            "replenishment_account_id": 1
        }
    },
    {
        "model": Income,
        "data": {
            "name": "test",
            "currency": "RUB",
            "amount": Decimal(1.5),
            "replenishment_account_id": 1
        }
    }
)


@pytest_asyncio.fixture(scope="session")
def event_loop(request) -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def db_engine() -> AsyncEngine:
    engine = create_async_engine(TEST_DATABASE_URL)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def session(db_engine: AsyncEngine) -> AsyncSession:
    async_session = sessionmaker(bind=db_engine, expire_on_commit=False, class_=AsyncSession)
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        async with async_session(bind=conn) as session:
            yield session
            await session.rollback()


@pytest_asyncio.fixture(scope="session")
async def seed_db(session: AsyncSession) -> None:
    accounts = await session.execute(select(Account))
    if not accounts.scalars().all():
        for entity in PRELOAD_DATA:
            new_table = entity["model"](**entity["data"])
            session.add(new_table)
        await session.commit()


@pytest_asyncio.fixture(scope="session")
def override_get_async_session(session: AsyncSession) -> Callable:
    async def _override_get_async_session():
        yield session

    return _override_get_async_session


@pytest_asyncio.fixture(scope="session")
def test_app(override_get_async_session: Callable) -> FastAPI:
    app.dependency_overrides[get_async_session] = override_get_async_session
    return app


@pytest_asyncio.fixture(scope="session")
async def client(seed_db, test_app: FastAPI) -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        yield ac

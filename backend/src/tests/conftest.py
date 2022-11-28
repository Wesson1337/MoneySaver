import asyncio
import os
from typing import Generator, Callable
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from backend.src.budget.models import Base

TEST_DATABASE_URL = f"{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@" \
                    f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('TEST_POSTGRES_DB')}"


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
    pass


@pytest_asyncio.fixture(scope="session")
def override_get_async_session(session: AsyncSession) -> Callable:
    async def _override_get_async_session():
        yield session

    return _override_get_async_session


@pytest_asyncio.fixture(scope="session")
async def client(seed_db, app: FastAPI) -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        yield ac

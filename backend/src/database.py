import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import DATABASE_URL

SQL_ALCHEMY_DATABASE_URL = f"postgresql+asyncpg://" + DATABASE_URL

engine = create_async_engine(
    SQL_ALCHEMY_DATABASE_URL, echo=bool(os.getenv('DEBUG')), connect_args={'check_same_thread': True}
)

async_session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base(engine)


async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session

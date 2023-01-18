from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from . import config

SQL_ALCHEMY_DATABASE_URL = "postgresql+asyncpg://" + config.DATABASE_URL

engine = create_async_engine(
    SQL_ALCHEMY_DATABASE_URL, echo=config.DEBUG
)

async_session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base(engine)

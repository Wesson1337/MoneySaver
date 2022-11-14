import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

SQL_ALCHEMY_DATABASE_URL = f"posgresql+asyncpg://" \
                           f"{os.getenv('DB_USER')}:" \
                           f"{os.getenv('DB_PASSWORD')}@" \
                           f"{os.getenv('DB_HOST')}:" \
                           f"{os.getenv('DB_PORT')}/" \
                           f"{os.getenv('DB_DATABASE')}"

engine = create_async_engine(
    SQL_ALCHEMY_DATABASE_URL, echo=os.getenv('DEBUG'), connect_args={'check_same_thread': True}
)

async_session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base(engine)

import os
from enum import Enum


def get_db_url() -> str:
    user = os.getenv('POSTGRES_USER') or 'postgres'
    password = os.getenv('POSTGRES_PASSWORD') or 'postgres'
    host = os.getenv('POSTGRES_HOST') or 'localhost'
    port = os.getenv('POSTGRES_PORT') or '5432'
    db = os.getenv('POSTGRES_DB') or 'postgres'

    return f"{user}:{password}@{host}:{port}/{db}"


DATABASE_URL = get_db_url()


class Currencies(Enum):
    """
    Enum type of currencies supported in app.
    IMPORTANT! If you change this, necessarily make new migration with 'alembic revision'
    """

    US = 1
    RUB = 2
    CNY = 3


class AccountTypes(Enum):
    """
    Enum type of account types supported in app.
    IMPORTANT! If you change this, necessarily make new migration with 'alembic revision'
    """

    WALLET = 1
    BANK_ACCOUNT = 2

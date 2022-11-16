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


class Currencies(str, Enum):
    """
    Enum type of currencies supported in app.
    IMPORTANT! If you change this, necessarily make new migration with 'alembic revision'
    """

    US = 'US'
    RUB = 'RUB'
    CNY = 'CNY'


class AccountTypes(str, Enum):
    """
    Enum type of account types supported in app.
    IMPORTANT! If you change this, necessarily make new migration with 'alembic revision'
    """

    WALLET = 'WALLET'
    BANK_ACCOUNT = 'BANK_ACCOUNT'

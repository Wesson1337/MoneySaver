import os
from enum import Enum

DEFAULT_API_PREFIX = "/api/v1"


def get_db_url(test: bool = False) -> str:
    """Returns database url without dialect and driver,
    add 'dialect+driver://' before it to use in sqlalchemy"""
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    db = os.getenv('POSTGRES_DB')
    host = os.getenv('POSTGRES_HOST')
    port = os.getenv('POSTGRES_DEV_PORT')

    if test:
        host = os.getenv('POSTGRES_TEST_HOST')
        port = os.getenv('POSTGRES_TEST_PORT')

    return f"{user}:{password}@{host}:{port}/{db}"


DATABASE_URL = get_db_url()


class Currencies(str, Enum):
    """
    Enum type of currencies supported in app.
    """

    def __str__(self):
        return self.value

    USD = 'USD'
    RUB = 'RUB'
    CNY = 'CNY'


class AccountTypes(str, Enum):
    """
    Enum type of account types supported in app.
    """
    def __str__(self):
        return self.value

    WALLET = 'WALLET'
    BANK_ACCOUNT = 'BANK_ACCOUNT'

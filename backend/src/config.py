import os
from enum import Enum

DEFAULT_API_PREFIX = "/api/v1"


def get_db_url(test: bool = False) -> str:
    """Returns database url without dialect and driver,
    add 'dialect+driver://' before it to use in sqlalchemy"""

    user = os.getenv('POSTGRES_USER') or 'postgres'
    password = os.getenv('POSTGRES_PASSWORD') or 'postgres'
    db = os.getenv('POSTGRES_DB') or 'postgres'

    if test:
        host = os.getenv('POSTGRES_TEST_HOST') or 'localhost'
        if os.getenv('POSTGRES_TEST_HOST'):
            port = '5432'
        else:
            port = '8001'
    else:
        host = os.getenv('POSTGRES_HOST') or 'localhost'
        port = os.getenv('POSTGRES_DEV_PORT') or '5432'

    return f"{user}:{password}@{host}:{port}/{db}"


DATABASE_URL = get_db_url()


class Currencies(str, Enum):
    """
    Enum type of currencies supported in app.
    """
    def __str__(self):
        return str(self.value)

    USD = 'USD'
    RUB = 'RUB'
    CNY = 'CNY'


class AccountTypes(str, Enum):
    """
    Enum type of account types supported in app.
    """
    def __str__(self):
        return str(self.value)

    WALLET = 'WALLET'
    BANK_ACCOUNT = 'BANK_ACCOUNT'

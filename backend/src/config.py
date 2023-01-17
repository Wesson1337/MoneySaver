import logging
import os

DEFAULT_API_PREFIX = "/api/v1"

DEBUG = os.getenv("DEBUG")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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

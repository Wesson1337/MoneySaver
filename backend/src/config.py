import logging
import os

DEFAULT_API_PREFIX = "/api/v1"

DEBUG = bool(os.getenv("DEBUG"))

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
TEST_DATABASE_URL = get_db_url(test=True)

REDIS_URL = f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}"
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
TEST_REDIS_URL = f"redis://{os.getenv('TEST_REDIS_HOST')}:{os.getenv('TEST_REDIS_PORT')}"
TEST_REDIS_PASSWORD = os.getenv('TEST_REDIS_PASSWORD')
REDIS_CACHING_DURATION_SECONDS = 60 * 60 * 12  # 12 hours

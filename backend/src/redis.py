from typing import Type, Optional

import aioredis

from backend.src import config
from backend.src.database import Base

redis = aioredis.from_url(
    config.REDIS_URL, password=config.REDIS_PASSWORD, decode_responses=True
)


def prefixed_key(f):
    """
    A method decorator that prefixes return values.
    Prefixes any string that the decorated method `f` returns with the value of
    the `prefix` attribute on the owner object `self`.
    """

    def prefixed_method(*args, **kwargs):
        self = args[0]
        key = f(*args, **kwargs)
        if self.prefix:
            return f'{self.prefix}:{key}'
        else:
            return key

    return prefixed_method


class Keys:
    """Methods to generate key names for Redis data structures."""
    def __init__(self, prefix: Optional[str] = None, sql_model: Optional[Type[Base]] = None):
        self.prefix = prefix
        self.model = sql_model

    @prefixed_key
    def sql_model_key_by_id(self, model_id: int):
        return f"{self.model.__tablename__}:{model_id}"


# TODO create get_cache and set_cache

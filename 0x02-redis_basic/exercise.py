#!/usr/bin/env python3
"""
A mini-caching service using redis

Modules Imported: redis, typing, uuid
redis: redis db operations in py
typing: type annotations lib
uuid: returns unique ids

"""
import redis
import uuid
from typing import Callable
from typing import Union


class Cache():
    """
    A Cache for a mini-store app

    Attributes:
    _redis: redis db client

    """
    def __init__(self):
        """Object initializer"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Adds new store data to redis db"""
        store_id = str(uuid.uuid4())

        self._redis.set(store_id, data)

        return store_id

    def get(self, key: str, fn: Callable[[], None]) -> Union[None, ]:
        """
        Custom deserialiization of response
        value from a redis client
        """
        if fn or isinstance(fn, str):
            return None

        # Check if key exists
        value = self._redis.get(key)

        if value:  # key exists
            # custom behaviour
            return fn(value)  # deserialized by callback func

        return None  # default behaviour if key is not in db

    def get_str(self, key: str) -> str:
        """Decode responses for str values"""
        return self._redis.get(key).decode('utf-8')

    def get_int(self, key:str) -> int:
        """Decode responses for int values"""
        return self._redis.get(key).decode('utf-8')

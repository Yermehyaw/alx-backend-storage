#!/usr/bin/env python3
"""
A mini-caching service using redis

Modules Imported: redis, typing, uuid
redis: redis db operations in py
typing: type annotations lib
uuid: returns unique ids

"""
from functools import wraps
import redis
import uuid
from typing import Any
from typing import Callable
from typing import Optional
from typing import Union
from typing import Tuple
from typing import TypeVar
from typing import Dict


def count_calls(method: Callable) -> Callable:
    """Decorator to count the number of times a method is called"""

    @wraps(method)
    def wrapper(self, *args, **kwargs) -> str:
        """Wrapper func"""
        self._redis.incr(method.__qualname__)

        return method(self, *args, **kwargs)  # execute methd and ret val

    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorates a method to store the history of its inputs and outputs"""

    @wraps(method)
    def wrapper(self, *args, **kwargs) -> str:
        """Wrapper to implemnt the decorator logic"""
        # Create a redis list of inputs to the method
        self._redis.rpush(method.__qualname__ + ':inputs', str(args))

        method_result = method(self, *args, **kwargs)

        # Create a redisdb list of output from method
        self._redis.rpush(method.__qualname__ + ':outputs', method_result)

        return method_result

    return wrapper


def replay(method: Callable) -> None:
    """Displays the history of calls of a particular function"""

    instance = method.__self__  # access the method's instance
    client = instance._redis
    mthd_name = method.__qualname__  # qualified name
    print(type(mthd_name))

    input_history = list(client.lrange(method.__qualname__ + ':inputs', 0, -1))
    output_history = list(client.lrange(method.__qualname__ + ':outputs'))
    no_calls = int(client.get(method.__qualname__))

    # Display format
    print(f'Cache.store was called {no_calls} times')
    for arg, ret in zip(input_history, output_history):
        print("Cache.store(*({arg})) -> {ret}")


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

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Adds new store data to redis db"""
        store_id = str(uuid.uuid4())

        self._redis.set(store_id, data)

        return store_id

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """
        Custom deserialiization of response
        value from a redis client
        """
        value = self._redis.get(key)

        if value and fn:
            # custom behaviour
            return fn(value)  # decoded by callback func

        return value  # defaut behaviour if fn isnt passed

    def get_str(self, value: bytes) -> str:
        """Decode responses for str values"""
        return value.decode('utf-8')

    def get_int(self, value: bytes) -> int:
        """Decode responses for int values"""
        return value.decode('utf-8')

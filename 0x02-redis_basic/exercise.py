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
from typing import Union
from typing import Tuple
from typing import TypeVar
from typing import Dict


C = TypeVar('C', bound='Cache')
R = TypeVar('R')


def count_calls(method: Callable[[C, Any], R]) -> Callable[[C, Any], R]:
    """Counts the number of times a method is called"""

    @wraps(method)
    def wrapper(self, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> str:
        """Wrapper func"""
        client = self._redis
        # create a count key with __qualname__ with an initial value of 0
        client.incr(method.__qualname__)
        method_result = func(*args, **kwargs)  # call the func/method to be wrapped

        return method_result

    return wrapper

def call_history(method: Callable[[C, Any], R]) -> Callable[[C, Any], R]:
    """Stores history of inputs and outputs of a method"""

    @wraps(method)
    def wrapper(self, *args, **kwargs) -> str:
        client = self._redis

        # Create a redis db list of inputs to the method
        client.rpush(method.__qualname__ + ':inputs', str(args))  # args to be saved a list of str rep of a list

        method_result = func(*args, **kwargs)

        # Create a redisdb list of output from method
        client.rpush(method.__qualname__ + ':outputs', method_result)

        return method_result  # return the expected return val of the decorated mthd

    return wrapper
        
        
    

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

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Adds new store data to redis db"""
        store_id = str(uuid.uuid4())

        self._redis.set(store_id, data)

        return store_id

    def get(self, key: str, fn: Callable[[], None]=None) -> Union[None, ]:
        """
        Custom deserialiization of response
        value from a redis client
        """
        if not fn or isinstance(fn, str):
            return None

        byte_key = bytes(key.decode('utf-8'))
        print(byte_key)
        if self._redis.type(key) == byte_key:
            # if key is in bytes, return in bytes
            return bytes(self._redis.get(key))

        # Check if key exists
        value = self._redis.get(key)

        if value:  # key exists
            # custom behaviour
            return fn(value)  # decoded by callback func

        return None  # default behaviour if key is not in db

    def get_str(self, key: str) -> str:
        """Decode responses for str values"""
        if self._redis.type(key) == 'bytes':
            return self._redis.get(key)

        return self._redis.get(key).decode('utf-8')

    def get_int(self, key:str) -> int:
        """Decode responses for int values"""
        if self._redis.type(key) == 'bytes':
            return self._redis.get(key)

        return self._redis.get(key).decode('utf-8')        

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


def count_calls(method: Callable[[Union[str, bytes, int, float]], str]) -> Callable[[Any], str]:
    """Decorator to count the number of times a method is called"""

    @wraps(method)
    def wrapper(self, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> str:
        """Wrapper func"""
        client = self._redis
        # create a count key with __qualname__ with an initial value of 0
        client.incr(method.__qualname__)

        return method(self, *args, **kwargs)  # call and return from the method to be wrapped

    return wrapper

def call_history(method: Callable[[C, Any], R]) -> Callable[[C, Any], R]:
    """Decorates a method to store the history of its inputs and outputs"""

    @wraps(method)
    def wrapper(self, *args, **kwargs) -> str:
        """Wrapper to implemnt the decorator logic"""
        client = self._redis

        return method(self, *args, **kwargs)  # return the expected return val of the decorated mthd

        # Create a redis db list of inputs to the method
        client.rpush(method.__qualname__ + ':inputs', str(*args))  # arg is a list 

        # Create a redisdb list of output from method
        client.rpush(method.__qualname__ + ':outputs', method_result)

    return wrapper


def replay(method: Callable[[C, Any], R]) -> None:
    """Displays the history of calls of a particular function"""

    instance = method.__self__  # access the instance which the method was called from
    client = instance._redis
    
    input_history = list(client.lrange(method.__qualname__ + ':inputs', 0, -1))  # retrieve the entire list from 0 to -1(end idx)
    output_history = list(client.lrange(method.__qualname__ + ':outputs'))  # equiv to previous lrange() call
    no_calls = int(client.get(method.__qualname__))

    # Display format
    print(f'Cache.store was called {no_calls} times')  # decorator is for store() mthd
    for arg, ret in zip(input_history, output_history):
        print("Cache.store(*('{arg}',)) -> {ret}")


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

    def get(self, key: str, fn: Callable[[], None]=None) -> Union[bytes, None]:
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

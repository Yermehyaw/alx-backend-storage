#!/usr/bin/env python3
"""
A mini-caching service using redis

Modules Imported: redis, random, uuid
random: return random values
redis: redis db operations in py
uuid: returns unique ids

"""
import random
import redis
import uuid


class Cache():
    """
    A Cache for a mini-store app

    Attributes:
    _redis: redis db client

    """
    def __init_():
        """Object initializer"""
        self._redis: redis.client.Redis = redis.Redis()

    def store(data: [bytes, str, int, float]) -> str:
        """Adds new store data to redis db"""
        store_id = uuid.uuid4()

        self._redis.set({store_id: data})

        return str(store_id.int)

from core.cache.base import BaseBackend
from core.connection.redis import redis


class RedisBackend(BaseBackend):
    async def get(self, key: str) -> str:
        result = redis.get(key)
        return result

    async def set(self, value: str, key: str, ttl: int = None) -> None:
        redis.set(name=value, value=key, ex=ttl)

    def init(self, value: str, key: str, ttl: int = None) -> None:
        redis.set(name=value, value=key, ex=ttl)

    async def incr(self, key: str) -> None:
        redis.incr(key)

    async def delete(self, key: str) -> None:
        redis.getdel(key)

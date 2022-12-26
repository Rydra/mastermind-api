from typing import Any, Callable

from aiocache import caches
from aiocache.base import BaseCache
from aiocache.lock import RedLock

from config.settings import settings


class CacheProvider:
    def __init__(self, cache: BaseCache, lease: int = 2) -> None:
        self.cache = cache
        self.lease = lease

    async def get_or_update(
        self,
        key: str,
        f: Callable,
        args: list[Any] | None = None,
        kwargs: dict | None = None,
        namespace: str | None = None,
        ttl: int | float | None = None,
    ) -> Any:
        final_key = self.cache.build_key(key, namespace)
        value = await self.cache.get(final_key)
        if value is not None:
            return value

        async with RedLock(self.cache, final_key, self.lease):
            value = await self.cache.get(final_key)
            if value is not None:
                return value

            kwargs = kwargs or {}
            args = args or []
            result = await f(*args, **kwargs)

            await self.cache.set(final_key, result, ttl=ttl)

        return result

    async def delete(self, key: str, namespace: str | None = None) -> None:
        await self.cache.delete(key, namespace=namespace)


def init_cache() -> None:
    caches.set_config(
        {
            "default": {
                "cache": "aiocache.SimpleMemoryCache",
                "serializer": {"class": "aiocache.serializers.PickleSerializer"},
            },
            "redis_alt": {
                "cache": "aiocache.RedisCache",
                "endpoint": settings.redis_host,
                "port": settings.redis_port,
                "timeout": 1,
                "serializer": {"class": "aiocache.serializers.PickleSerializer"},
                "plugins": [
                    {"class": "aiocache.plugins.HitMissRatioPlugin"},
                    {"class": "aiocache.plugins.TimingPlugin"},
                ],
            },
        }
    )

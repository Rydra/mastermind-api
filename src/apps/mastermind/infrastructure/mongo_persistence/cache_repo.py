from typing import cast, Any

from aiocache import cached_stampede as base_cached_stampede, caches
from aiocache.base import BaseCache

from apps.mastermind.core.domain.domain import Game
from apps.mastermind.core.domain.interfaces import IGameRepository
from apps.shared.typing import Id


def cached_stampede(*args: Any, **kwargs: Any) -> Any:
    if "key" in kwargs and "namespace" in kwargs:
        key = ":".join([kwargs.pop("namespace"), kwargs.pop("key")])
        kwargs["key"] = key

    return base_cached_stampede(*args, **kwargs)


class CachedRepository(IGameRepository):
    """
    The cache stampede uses the proper caching strategy of lazy reads.
    """

    namespace = "games"

    def __init__(self, repository: IGameRepository) -> None:
        self.repository = repository

    def all(self) -> list[Game]:
        return []

    def save(self, game: Game) -> None:
        pass

    def get(self, id: int) -> Game:
        pass

    async def aall(self) -> list[Game]:
        return await cached_stampede(
            alias="redis_alt", noself=True, key="aall", namespace=self.namespace
        )(self.repository.aall)()

    def next_id(self) -> Id:
        return self.repository.next_id()

    async def aget(self, id: Id) -> Game:
        return await cached_stampede(
            alias="redis_alt", noself=True, key=f"aget-{id}", namespace=self.namespace
        )(self.repository.aget)(id)

    async def asave(self, game: Game) -> None:
        # Beware: save operations from a repository, if they are under
        # a unit of work session, will not do any physical save. When we save
        await self.repository.asave(game)
        cache = cast(BaseCache, caches.get("redis_alt"))
        await cache.delete("aall", namespace=self.namespace)
        await cache.delete(f"aget-{game.id}", namespace=self.namespace)
        await cache.delete(f"count", namespace=self.namespace)

    async def count(self) -> int:
        return await cached_stampede(
            alias="redis_alt", noself=True, key="count", namespace=self.namespace
        )(self.repository.count)()

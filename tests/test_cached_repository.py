from collections import defaultdict
from typing import Any

import pytest
from aiocache import caches
from hamcrest import *

from apps.mastermind.core.domain.domain import Game
from apps.mastermind.core.domain.interfaces import IGameRepository
from apps.mastermind.infrastructure.cache.cache_repo import CachedRepository
from apps.mastermind.infrastructure.mongo_persistence.session import Session
from apps.shared.anyio import async_to_sync
from apps.shared.cache import CacheProvider
from apps.shared.typing import Id


def awaitable(value: Any) -> Any:
    async def _(*args, **kwargs):
        return value

    return _


class GameRepositoryStub(IGameRepository):
    def __init__(self):
        self.call_counts = defaultdict(int)

    def next_id(self) -> Id:
        ...

    async def aall(self) -> list[Game]:
        self.call_counts["aall"] += 1
        return [Game.new(1, 1, 1)]

    async def count(self) -> int:
        ...

    async def asave(self, game: Game) -> None:
        ...

    async def aget(self, id: int) -> Game:
        self.call_counts["aget"] += 1
        return Game.new(1, 1, 1)


@pytest.mark.integrationtest
class TestCachedRepository:
    async def test_cache_all(self, anyio_backend, request):
        def clear_cache():
            async def _():
                return await caches.get("redis_alt").clear(namespace="games")

            async_to_sync(_)

        request.addfinalizer(clear_cache)
        game_repository_stub = GameRepositoryStub()
        cached_repository = CachedRepository(
            game_repository_stub, CacheProvider(caches.get("redis_alt")), Session()
        )

        await cached_repository.aall()
        await cached_repository.aall()

        assert_that(game_repository_stub.call_counts["aall"], is_(1))

    async def test_saving_clears_the_cache_for_listing(self, anyio_backend, request):
        def clear_cache():
            async def _():
                return await caches.get("redis_alt").clear(namespace="games")

            async_to_sync(_)

        request.addfinalizer(clear_cache)
        game_repository_stub = GameRepositoryStub()
        session = Session()
        cached_repository = CachedRepository(
            game_repository_stub, CacheProvider(caches.get("redis_alt")), session
        )

        await cached_repository.aall()
        await cached_repository.asave(Game.new(1, 1, 1, id="AAA"))
        await session.commit()

        await cached_repository.aall()

        assert_that(game_repository_stub.call_counts["aall"], is_(2))

    async def test_saving_clears_the_cache_for_individual_get(
        self, anyio_backend, request
    ):
        def clear_cache():
            async def _():
                return await caches.get("redis_alt").clear(namespace="games")

            async_to_sync(_)

        request.addfinalizer(clear_cache)
        game_repository_stub = GameRepositoryStub()

        session = Session()
        cached_repository = CachedRepository(
            game_repository_stub, CacheProvider(caches.get("redis_alt")), session
        )

        await cached_repository.aget("AAA")
        await cached_repository.asave(Game.new(1, 1, 1, id="AAA"))

        await session.commit()
        await cached_repository.aget("AAA")
        await cached_repository.aget("AAA")

        assert_that(game_repository_stub.call_counts["aget"], is_(2))

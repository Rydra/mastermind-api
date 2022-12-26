from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient

from apps.mastermind.infrastructure.mongo_persistence.repo import MongoGameRepository
from apps.mastermind.infrastructure.cache.cache_repo import CachedRepository
from apps.mastermind.infrastructure.mongo_persistence.session import Session
from apps.shared.cache import CacheProvider
from apps.shared.uow import IUnitOfWork
from config.settings import settings


class MongoUnitOfWork(IUnitOfWork):
    def __init__(self, cache_provider: CacheProvider) -> None:
        self.cache_provider = cache_provider

    async def __aenter__(self) -> "MongoUnitOfWork":
        client = AsyncIOMotorClient(settings.mongodb_dsm)
        self.session = Session()
        self.games = MongoGameRepository(client[settings.mongo_dbname], self.session)
        if settings.use_cache:
            self.games = CachedRepository(self.games, self.cache_provider, self.session)
        return self

    async def __aexit__(self, *args: Any) -> None:
        await super().__aexit__(*args)

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        pass

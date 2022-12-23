from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient

from apps.mastermind.infrastructure.mongo_persistence.repo import MongoGameRepository
from apps.shared.uow import IUnitOfWork
from config.settings import settings


class MongoUnitOfWork(IUnitOfWork):
    async def __aenter__(self) -> "MongoUnitOfWork":
        client = AsyncIOMotorClient(settings.mongodb_dsm)
        self.games = MongoGameRepository(client)
        return self

    async def __aexit__(self, *args: Any) -> None:
        await super().__aexit__(*args)

    async def commit(self) -> None:
        pass

    async def rollback(self) -> None:
        pass

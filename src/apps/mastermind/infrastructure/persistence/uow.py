from typing import Any

from asgiref.sync import sync_to_async
from django.db import transaction

from apps.mastermind.infrastructure.persistence.repo import GameRepository
from apps.shared.uow import IUnitOfWork


class DjangoUnitOfWork(IUnitOfWork):
    async def __aenter__(self) -> "DjangoUnitOfWork":
        self.games = GameRepository()
        await sync_to_async(transaction.set_autocommit)(False)
        return self

    async def __aexit__(self, *args: Any) -> None:
        await super().__aexit__(*args)
        await sync_to_async(transaction.set_autocommit)(True)

    async def commit(self) -> None:
        await sync_to_async(transaction.commit)()

    async def rollback(self) -> None:
        await sync_to_async(transaction.rollback)()

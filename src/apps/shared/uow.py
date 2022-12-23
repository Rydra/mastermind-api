import abc
from typing import Any

from apps.mastermind.core.domain.interfaces import IGameRepository


class IUnitOfWork(abc.ABC):
    games: IGameRepository

    async def __aenter__(self) -> "IUnitOfWork":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.rollback()

    @abc.abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError

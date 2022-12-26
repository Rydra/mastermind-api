import abc
from typing import Any, Callable

from apps.mastermind.core.domain.interfaces import IGameRepository


class BaseSession:
    def __init__(self) -> None:
        self.callbacks: list[Callable] = []

    def add_postcommit_hook(self, f: Callable) -> None:
        self.callbacks.append(f)

    async def _commit(self) -> None:
        raise NotImplementedError

    async def commit(self) -> None:
        await self._commit()
        await self.run_postcommit_hooks()

    async def run_postcommit_hooks(self) -> None:
        while self.callbacks:
            f = self.callbacks.pop()
            await f()


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

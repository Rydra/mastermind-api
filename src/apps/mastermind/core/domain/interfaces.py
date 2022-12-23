from abc import ABC, abstractmethod

from apps.mastermind.core.domain.domain import Game


class IGameRepository(ABC):
    @abstractmethod
    def all(self) -> list[Game]:
        ...

    @abstractmethod
    def save(self, game: Game) -> None:
        ...

    @abstractmethod
    def get(self, id: int) -> Game:
        ...

    @abstractmethod
    async def aall(self) -> list[Game]:
        ...

    @abstractmethod
    async def asave(self, game: Game) -> None:
        ...

    @abstractmethod
    async def aget(self, id: int) -> Game:
        ...

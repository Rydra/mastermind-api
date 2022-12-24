from abc import ABC, abstractmethod

from apps.mastermind.core.domain.domain import Game
from apps.shared.typing import Id


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
    def next_id(self) -> Id:
        ...

    @abstractmethod
    async def aall(self) -> list[Game]:
        ...

    @abstractmethod
    async def count(self) -> int:
        ...

    @abstractmethod
    async def asave(self, game: Game) -> None:
        ...

    @abstractmethod
    async def aget(self, id: int) -> Game:
        ...

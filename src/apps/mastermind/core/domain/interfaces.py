from abc import ABC, abstractmethod
from typing import List

from apps.mastermind.core.domain.domain import Game


class IGameRepository(ABC):
    @abstractmethod
    def all(self) -> List[Game]:
        ...

    @abstractmethod
    def save(self, game: Game) -> None:
        ...

    @abstractmethod
    def get(self, id: int) -> Game:
        ...

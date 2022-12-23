from typing import Callable

from apps.mastermind.infrastructure.mongo_persistence.uow import MongoUnitOfWork
from apps.mastermind.infrastructure.persistence.repo import GameRepository
import pinject


class MastermindBindingSpec(pinject.BindingSpec):
    def configure(self, bind: Callable) -> None:
        bind("game_repository", to_class=GameRepository)
        bind("uow", to_class=MongoUnitOfWork)

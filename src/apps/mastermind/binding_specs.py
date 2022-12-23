from typing import Callable

from apps.mastermind.infrastructure.persistence.repo import GameRepository
import pinject

from apps.mastermind.infrastructure.persistence.uow import DjangoUnitOfWork


class MastermindBindingSpec(pinject.BindingSpec):
    def configure(self, bind: Callable) -> None:
        bind("game_repository", to_class=GameRepository)
        bind("uow", to_class=DjangoUnitOfWork)

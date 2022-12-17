from typing import T, Type  # type: ignore

import pinject
from singleton import Singleton

from apps.mastermind.binding_specs import MastermindBindingSpec


class Container(metaclass=Singleton):
    def __init__(self) -> None:
        self.obj_graph = pinject.new_object_graph(
            modules=None,
            binding_specs=[MastermindBindingSpec()],
        )

    def provide(self, klass: Type[T]) -> T:
        return self.obj_graph.provide(klass)


def provide(klass: Type[T]) -> T:
    return Container().provide(klass)

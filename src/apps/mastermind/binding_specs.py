from typing import Callable

from aiocache import caches
from aiocache.base import BaseCache

from apps.mastermind.infrastructure.mongo_persistence.uow import MongoUnitOfWork
import pinject


class MastermindBindingSpec(pinject.BindingSpec):
    def configure(self, bind: Callable) -> None:
        bind("uow", to_class=MongoUnitOfWork)

    def provide_cache(self) -> BaseCache:
        return caches.get("redis_alt")

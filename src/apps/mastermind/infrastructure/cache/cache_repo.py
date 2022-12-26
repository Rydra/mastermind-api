from apps.mastermind.core.domain.domain import Game
from apps.mastermind.core.domain.interfaces import IGameRepository
from apps.mastermind.infrastructure.mongo_persistence.session import Session
from apps.shared.cache import CacheProvider
from apps.shared.typing import Id


class CachedRepository(IGameRepository):
    """
    The cache stampede uses the proper caching strategy of lazy reads.
    """

    namespace = "games"

    def __init__(
        self, repository: IGameRepository, cache: CacheProvider, session: Session
    ) -> None:
        self.repository = repository
        self.cache = cache
        self.session = session

    async def aall(self) -> list[Game]:
        return await self.cache.get_or_update(
            "aall",
            namespace=self.namespace,
            f=self.repository.aall,
        )

    def next_id(self) -> Id:
        return self.repository.next_id()

    async def aget(self, id: Id) -> Game:
        return await self.cache.get_or_update(
            f"aget-{id}", namespace=self.namespace, f=self.repository.aget, args=(id,)
        )

    async def asave(self, game: Game) -> None:
        # Beware: save operations from a repository, if they are under
        # a unit of work session, will not do any physical save. When we save
        await self.repository.asave(game)
        self.session.add_postcommit_hook(
            lambda: self.cache.delete("aall", namespace=self.namespace)
        )
        self.session.add_postcommit_hook(
            lambda: self.cache.delete(f"aget-{game.id}", namespace=self.namespace)
        )
        self.session.add_postcommit_hook(
            lambda: self.cache.delete(f"count", namespace=self.namespace)
        )

    async def count(self) -> int:
        return await self.cache.get_or_update(
            "count", namespace=self.namespace, f=self.repository.count
        )

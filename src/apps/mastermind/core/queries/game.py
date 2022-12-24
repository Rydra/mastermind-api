from asyncio import TaskGroup

from apps.shared.interfaces import Query
from apps.mastermind.core.domain.domain import Game, ListResult
from apps.shared.typing import Id
from apps.shared.uow import IUnitOfWork


class ListGames(Query):
    pass


class ListGamesHandler:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def run(self, command: ListGames) -> ListResult[Game]:
        async with self.uow:
            async with TaskGroup() as tg:
                games = tg.create_task(self.uow.games.aall())
                count = tg.create_task(self.uow.games.count())

        return ListResult(count=count.result(), results=games.result())


class GetGame(Query):
    id: Id


class GetGameHandler:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def run(self, command: GetGame) -> Game:
        async with self.uow:
            game = await self.uow.games.aget(command.id)
            return game

from apps.shared.anyio import ResultGatheringTaskgroup
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
            async with ResultGatheringTaskgroup() as tg:
                games = tg.start_soon(self.uow.games.aall)
                count = tg.start_soon(self.uow.games.count)

        return ListResult(count=tg.get_result(count), results=tg.get_result(games))


class GetGame(Query):
    id: Id


class GetGameHandler:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def run(self, command: GetGame) -> Game:
        async with self.uow:
            game = await self.uow.games.aget(command.id)
            return game

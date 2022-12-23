from apps.shared.interfaces import Query
from apps.mastermind.core.domain.domain import Game
from apps.shared.typing import Id
from apps.shared.uow import IUnitOfWork


class ListGames(Query):
    pass


class ListGamesHandler:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def run(self, command: ListGames) -> list[Game]:
        async with self.uow:
            games = await self.uow.games.aall()
            return games


class GetGame(Query):
    id: Id


class GetGameHandler:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def run(self, command: GetGame) -> Game:
        async with self.uow:
            game = await self.uow.games.aget(command.id)
            return game

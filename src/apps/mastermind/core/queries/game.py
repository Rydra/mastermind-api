from typing import List

from apps.mastermind.core.domain.interfaces import IGameRepository
from apps.shared.interfaces import Query
from apps.mastermind.core.domain.domain import Game


class ListGames(Query):
    pass


class ListGamesHandler:
    def __init__(self, game_repository: IGameRepository) -> None:
        self.game_repository = game_repository

    async def run(self, command: ListGames) -> List[Game]:
        games = await self.game_repository.aall()
        return games


class GetGame(Query):
    id: int


class GetGameHandler:
    def __init__(self, game_repository: IGameRepository) -> None:
        self.game_repository = game_repository

    async def run(self, command: GetGame) -> Game:
        game = await self.game_repository.aget(command.id)
        return game

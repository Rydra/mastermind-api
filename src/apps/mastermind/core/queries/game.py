from typing import List

from apps.shared.interfaces import Query
from apps.mastermind.core.domain.domain import Game
from apps.mastermind.persistence.repo import GameRepository


class ListGames(Query):
    pass


class ListGamesHandler:
    def __init__(self, game_repository: GameRepository) -> None:
        self.game_repository = game_repository

    def run(self, command: ListGames) -> List[Game]:
        games = self.game_repository.all()
        return games


class GetGame(Query):
    id: int


class GetGameHandler:
    def __init__(self, game_repository: GameRepository) -> None:
        self.game_repository = game_repository

    def run(self, command: GetGame) -> Game:
        game = self.game_repository.get(command.id)
        return game

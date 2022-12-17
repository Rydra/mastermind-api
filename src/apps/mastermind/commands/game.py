from typing import List

from apps.infrastructure.interfaces import Command
from apps.mastermind.domain.domain import Game
from apps.mastermind.repo import Games


class CreateGame(Command):
    num_slots: int
    num_colors: int
    max_guesses: int


class CreateGameHandler:
    def __init__(self, game_repository: Games) -> None:
        self.game_repository = game_repository

    def run(self, command: CreateGame) -> Game:
        game = Game.new(command.num_slots, command.num_colors, command.max_guesses)
        self.game_repository.save(game)
        return game


class AddGuess(Command):
    id: int
    code: List[str]


class AddGuessHandler:
    def __init__(self, game_repository: Games) -> None:
        self.game_repository = game_repository

    def run(self, command: AddGuess) -> Game:
        game = self.game_repository.get(command.id)
        game.add_guess(command.code)
        self.game_repository.save(game)
        return game

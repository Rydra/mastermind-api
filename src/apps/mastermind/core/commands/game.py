from typing import List

from apps.mastermind.core.domain.interfaces import IGameRepository
from apps.shared.interfaces import Command
from apps.mastermind.core.domain.domain import Game


class CreateGame(Command):
    num_slots: int
    num_colors: int
    max_guesses: int


class CreateGameHandler:
    def __init__(self, game_repository: IGameRepository) -> None:
        self.game_repository = game_repository

    async def run(self, command: CreateGame) -> Game:
        game = Game.new(command.num_slots, command.num_colors, command.max_guesses)
        await self.game_repository.asave(game)
        return game


class AddGuess(Command):
    id: int
    code: List[str]


class AddGuessHandler:
    def __init__(self, game_repository: IGameRepository) -> None:
        self.game_repository = game_repository

    async def run(self, command: AddGuess) -> Game:
        game = await self.game_repository.aget(command.id)
        game.add_guess(command.code)
        await self.game_repository.asave(game)
        return game

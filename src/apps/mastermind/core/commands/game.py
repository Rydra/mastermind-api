from apps.shared.interfaces import Command
from apps.mastermind.core.domain.domain import Game, Color
from apps.shared.typing import Id
from apps.shared.uow import IUnitOfWork


class CreateGame(Command):
    num_slots: int
    num_colors: int
    max_guesses: int


class CreateGameHandler:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def run(self, command: CreateGame) -> Game:
        async with self.uow:
            game = Game.new(
                command.num_slots,
                command.num_colors,
                command.max_guesses,
                id=self.uow.games.next_id(),
            )
            await self.uow.games.asave(game)
            await self.uow.commit()

        return game


class AddGuess(Command):
    id: Id
    code: list[Color]


class AddGuessHandler:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def run(self, command: AddGuess) -> Game:
        async with self.uow:
            game = await self.uow.games.aget(command.id)
            game.add_guess(command.code)
            await self.uow.games.asave(game)
            await self.uow.commit()

        return game

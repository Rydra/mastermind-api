import strawberry
from typing import TypeAlias

from apps.mastermind.core.commands.game import CreateGame, AddGuess
from apps.mastermind.infrastructure.graphql.shared import ColorEnum
from apps.shared.command_bus import CommandBus


@strawberry.type
class MutationResult:
    ok: bool
    error: str | None


@strawberry.type
class GameCreatedSuccess:
    id: str


@strawberry.type
class AddGuessSuccess:
    ok: bool


@strawberry.type
class Error:
    reason: str


CreateGameResponse: TypeAlias = strawberry.union(  # type: ignore
    "CreateGameResponse", [GameCreatedSuccess, Error]  # type: ignore
)

AddGuessResponse: TypeAlias = strawberry.union(  # type: ignore
    "AddGuessResponse", [AddGuessSuccess, Error]
)


@strawberry.input
class CreateGameInput:
    num_slots: int
    num_colors: int
    max_guesses: int | None = 10


@strawberry.input
class AddGuessInput:
    game_id: str
    code: list[ColorEnum]


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_game(self, input: CreateGameInput) -> CreateGameResponse:
        try:
            command = CreateGame(
                num_slots=input.num_slots,
                num_colors=input.num_colors,
                max_guesses=input.max_guesses,
            )
            game = await CommandBus().asend(command)

            return GameCreatedSuccess(id=game.id)
        except Exception as e:
            return Error(reason=str(e))

    @strawberry.mutation
    async def add_guess(self, input: AddGuessInput) -> AddGuessResponse:
        try:
            await CommandBus().asend(AddGuess(id=input.game_id, code=input.code))
            return AddGuessSuccess(ok=True)
        except Exception as e:
            return Error(reason=str(e))

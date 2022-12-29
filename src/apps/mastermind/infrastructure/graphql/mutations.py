import strawberry
from typing import TypeAlias

from pyvaru import ValidationException

from apps.auth.infrastructure.graphql.context import IsAuthenticated
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
class ErrorMessage:
    label: str
    error_messages: list[str]


@strawberry.type
class ValidationError:
    message: str
    errors: list[ErrorMessage]

    @staticmethod
    def from_exception(e: ValidationException) -> "ValidationError":
        return ValidationError(
            message=e.message,
            errors=[
                ErrorMessage(label=label, error_messages=error_messages)
                for label, error_messages in e.validation_result.errors.items()
            ],
        )


@strawberry.type
class Error:
    reason: str


CreateGameResponse: TypeAlias = strawberry.union(  # type: ignore
    "CreateGameResponse", [GameCreatedSuccess, ValidationError, Error]  # type: ignore
)

AddGuessResponse: TypeAlias = strawberry.union(  # type: ignore
    "AddGuessResponse", [AddGuessSuccess, ValidationError, Error]
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
class MastermindMutations:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
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

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def add_guess(self, input: AddGuessInput) -> AddGuessResponse:
        try:
            await CommandBus().asend(AddGuess(id=input.game_id, code=input.code))
            return AddGuessSuccess(ok=True)
        except ValidationException as e:
            return ValidationError.from_exception(e)
        except Exception as e:
            return Error(reason=str(e))

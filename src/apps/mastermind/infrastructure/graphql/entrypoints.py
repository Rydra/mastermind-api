from typing import Generic, cast, TypeAlias

import strawberry
from strawberry.asgi import GraphQL

from apps.mastermind.core.commands.game import CreateGame, AddGuess
from apps.mastermind.core.queries.game import (
    ListGamesHandler,
    ListGames,
    GetGameHandler,
    GetGame,
)
from apps.mastermind.infrastructure.graphql.nodes import GameNode
from apps.shared.command_bus import CommandBus
from apps.shared.exceptions import NotFound
from apps.shared.typing import T
from composite_root.container import provide


class Page(Generic[T]):  # type: ignore
    count: int
    results: list[T]


@strawberry.type
class Query:
    @strawberry.field
    async def games(self) -> list[GameNode]:
        games = await provide(ListGamesHandler).run(ListGames())
        return cast(list[GameNode], games)

    @strawberry.field
    async def game(self, id: str) -> GameNode | None:
        try:
            game = await provide(GetGameHandler).run(GetGame(id=id))
            return cast(GameNode, game)
        except NotFound:
            return None


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
    code: list[str]


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


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQL(schema)

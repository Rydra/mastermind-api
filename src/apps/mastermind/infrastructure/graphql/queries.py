from typing import cast, Generic

import strawberry

from apps.mastermind.core.queries.game import (
    ListGamesHandler,
    ListGames,
    GetGameHandler,
    GetGame,
)
from apps.mastermind.infrastructure.graphql.shared import ColorEnum, GameStateEnum
from apps.shared.exceptions import NotFound
from apps.shared.typing import T
from composite_root.container import provide

from apps.mastermind.core.domain.domain import Guess, Game


@strawberry.type
class Page(Generic[T]):  # type: ignore
    count: int
    results: list[T]


@strawberry.type
class GuessNode:
    code: list[ColorEnum]
    black_pegs: int
    white_pegs: int

    @staticmethod
    def from_domain(guess: Guess) -> "GuessNode":
        return GuessNode(
            code=guess.code, black_pegs=guess.black_pegs, white_pegs=guess.white_pegs
        )


@strawberry.type
class GameNode:
    id: str
    reference: str
    num_colors: int
    num_slots: int
    max_guesses: int
    colors: list[ColorEnum]
    state: GameStateEnum
    secret_code: list[ColorEnum]
    allowed_colors: list[ColorEnum]
    guesses: list[GuessNode]

    @staticmethod
    def from_domain(game: Game) -> "GameNode":
        return GameNode(
            id=game.id,
            reference=game.reference,
            num_colors=game.num_colors,
            num_slots=game.num_slots,
            max_guesses=game.max_guesses,
            colors=game.colors,
            state=game.state,
            secret_code=game.secret_code,
            allowed_colors=game.allowed_colors,
            guesses=[GuessNode.from_domain(guess) for guess in game.guesses],
        )


@strawberry.type
class Query:
    @strawberry.field
    async def games(self) -> Page[GameNode]:  # type: ignore
        games = await provide(ListGamesHandler).run(ListGames())
        return Page(count=games.count, results=games.results)

    @strawberry.field
    async def game(self, id: str) -> GameNode | None:
        try:
            game = await provide(GetGameHandler).run(GetGame(id=id))
            return cast(GameNode, game)
        except NotFound:
            return None

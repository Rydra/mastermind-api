from pydantic import BaseModel

from apps.mastermind.core.domain.domain import Game, Guess, Color
from apps.shared.typing import Id


class GuessDto(BaseModel):
    code: list[Color]
    black_pegs: int
    white_pegs: int

    @staticmethod
    def from_domain(guess: Guess) -> "GuessDto":
        return GuessDto(
            code=guess.code, black_pegs=guess.black_pegs, white_pegs=guess.white_pegs
        )


class GameDto(BaseModel):
    id: Id
    reference: str
    num_colors: int
    num_slots: int
    max_guesses: int = 10
    colors: list[Color]
    status: str
    secret_code: list[Color]
    allowed_colors: list[Color]
    guesses: list[GuessDto]

    @staticmethod
    def from_domain(game: Game) -> "GameDto":
        return GameDto(
            id=game.id,
            reference=game.reference,
            num_colors=game.num_colors,
            num_slots=game.num_slots,
            max_guesses=game.max_guesses,
            colors=game.colors,
            status=game.status,
            secret_code=game.secret_code,
            allowed_colors=game.allowed_colors,
            guesses=[GuessDto.from_domain(guess) for guess in game.guesses],
        )


class ListGamesResponse(BaseModel):
    results: list[GameDto]


class CreateGameRequest(BaseModel):
    num_slots: int
    num_colors: int
    max_guesses: int = 10


class AddGuessRequest(BaseModel):
    code: list[Color]

from typing import List

from pydantic import BaseModel

from apps.mastermind.core.domain.domain import Game, Guess


class GuessDto(BaseModel):
    code: List[str]
    black_pegs: int
    white_pegs: int

    @staticmethod
    def from_domain(guess: Guess) -> "GuessDto":
        return GuessDto(
            code=guess.code, black_pegs=guess.black_pegs, white_pegs=guess.white_pegs
        )


class GameDto(BaseModel):
    id: int
    reference: str
    num_colors: int
    num_slots: int
    max_guesses: int = 10
    colors: List[str]
    status: str
    secret_code: List[str]
    guesses: List[GuessDto]

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
            guesses=[GuessDto.from_domain(guess) for guess in game.guesses],
        )


class ListGamesResponse(BaseModel):
    results: List[GameDto]


class CreateGameRequest(BaseModel):
    num_slots: int
    num_colors: int
    max_guesses: int = 10


class AddGuessRequest(BaseModel):
    code: List[str]

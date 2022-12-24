import strawberry

from apps.mastermind.core.domain.domain import Guess, Game


@strawberry.type
class GuessNode:
    code: list[str]
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
    colors: list[str]
    status: str
    secret_code: list[str]
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
            status=game.status,
            secret_code=game.secret_code,
            guesses=[GuessNode.from_domain(guess) for guess in game.guesses],
        )

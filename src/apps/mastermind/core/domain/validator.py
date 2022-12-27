from typing import cast

from pyvaru import ValidationRule, Validator

from apps.mastermind.core.domain.domain import Color, Game, GameState


class CodeIsValidForGame(ValidationRule):
    def apply(self) -> bool | tuple[bool, str]:
        code = cast(list[Color], self.apply_to["code"])
        game = cast(Game, self.apply_to["game"])

        return (
            len(code) == game.num_slots
            and len(set(code) - set(game.allowed_colors)) == 0
        )


class GameIsRunning(ValidationRule):
    def apply(self) -> bool | tuple[bool, str]:
        game = cast(Game, self.apply_to["game"])

        return game.state == GameState.RUNNING


class AddGuessValidator(Validator):
    def get_rules(self, data: dict) -> list:
        return [
            CodeIsValidForGame(
                {"code": data["code"], "game": data["game"]},
                label="code_is_valid",
                error_message="The guess has some invalid colors for this game, or does "
                "not have the appropriate length",
            ),
            GameIsRunning(
                {"game": data["game"]},
                label="game_is_running",
                error_message="Cannot add a new guess, the game is already finished",
            ),
        ]

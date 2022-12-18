import pytest
from hamcrest import *
from apps.mastermind.core.domain.domain import Game
from apps.mastermind.persistence.repo import GameRepository


@pytest.mark.django_db
class TestGameRepository:
    async def test_save_new_game(self, anyio_backend):
        sut = GameRepository()
        game = Game.new(num_slots=2, max_guesses=10, num_colors=4)
        await sut.asave(game)

        game_from_db = await sut.aget(game.id)
        assert_that(
            game_from_db,
            has_properties(
                reference=is_(str),
                num_slots=game.num_slots,
                max_guesses=10,
                num_colors=4,
                secret_code=game.secret_code,
                status=game.status,
            ),
        )

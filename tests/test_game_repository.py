import pytest
from hamcrest import *
from apps.mastermind.core.domain.domain import Game
from apps.mastermind.infrastructure.persistence.repo import GameRepository
from apps.mastermind.infrastructure.persistence.uow import DjangoUnitOfWork


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
                state=game.state,
            ),
        )

    async def test_save_new_game_with_uow(self, anyio_backend):
        uow = DjangoUnitOfWork()
        game = Game.new(num_slots=2, max_guesses=10, num_colors=4)
        async with uow:
            await uow.games.asave(game)
            await uow.commit()
            game_from_db = await uow.games.aget(game.id)

        assert_that(
            game_from_db,
            has_properties(
                reference=is_(str),
                num_slots=game.num_slots,
                max_guesses=10,
                num_colors=4,
                state=game.state,
            ),
        )

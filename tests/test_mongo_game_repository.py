from hamcrest import *

from apps.mastermind.core.domain.domain import Game
from apps.mastermind.infrastructure.mongo_persistence.uow import MongoUnitOfWork


class TestMongoGameRepository:
    async def test_save_new_game_with_uow(self, anyio_backend):
        uow = MongoUnitOfWork()
        async with uow:
            game = Game.new(num_slots=2, max_guesses=10, num_colors=4)
            game.add_guess(["red", "red"])
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
                    secret_code=game.secret_code,
                    status=game.status,
                    guesses=contains_exactly(has_properties(code=["red", "red"])),
                ),
            )

    async def test_save_update_game_with_uow(self, anyio_backend):
        uow = MongoUnitOfWork()
        async with uow:
            new_game = Game.new(num_slots=2, max_guesses=10, num_colors=4)
            new_game.add_guess(["red", "red"])
            await uow.games.asave(new_game)

        async with uow:
            game = await uow.games.aget(new_game.id)
            game.add_guess(["green", "green"])
            await uow.games.asave(game)
            await uow.commit()

            game_from_db = await uow.games.aget(game.id)
            assert_that(
                game_from_db,
                has_properties(
                    id=new_game.id,
                    reference=is_(str),
                    num_slots=game.num_slots,
                    max_guesses=10,
                    num_colors=4,
                    secret_code=game.secret_code,
                    status=game.status,
                    guesses=contains_exactly(
                        has_properties(code=["red", "red"]),
                        has_properties(code=["green", "green"]),
                    ),
                ),
            )

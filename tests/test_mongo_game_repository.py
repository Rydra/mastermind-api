from hamcrest import *

from apps.mastermind.core.domain.domain import Game, Color
from apps.mastermind.infrastructure.mongo_persistence.uow import MongoUnitOfWork
from composite_root.container import provide


class TestMongoGameRepository:
    async def test_save_new_game_with_uow(self, anyio_backend):
        uow = provide(MongoUnitOfWork)
        async with uow:
            game = Game.new(
                num_slots=2, max_guesses=10, num_colors=4, id=uow.games.next_id()
            )
            game.add_guess([Color.RED, Color.RED])
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
                    state=game.state,
                    guesses=contains_exactly(
                        has_properties(code=[Color.RED, Color.RED])
                    ),
                ),
            )

    async def test_save_update_game_with_uow(self, anyio_backend):
        uow = provide(MongoUnitOfWork)
        async with uow:
            new_game = Game.new(
                num_slots=2, max_guesses=10, num_colors=4, id=uow.games.next_id()
            )
            new_game.add_guess([Color.RED, Color.RED])
            await uow.games.asave(new_game)
            await uow.commit()

        async with uow:
            game = await uow.games.aget(new_game.id)
            game.add_guess([Color.GREEN, Color.GREEN])
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
                    state=game.state,
                    guesses=contains_exactly(
                        has_properties(code=[Color.RED, Color.RED]),
                        has_properties(code=[Color.GREEN, Color.GREEN]),
                    ),
                ),
            )

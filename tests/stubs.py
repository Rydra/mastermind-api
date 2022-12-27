from apps.mastermind.core.domain.domain import Color, Game
from apps.mastermind.infrastructure.mongo_persistence.uow import MongoUnitOfWork
from composite_root.container import provide


class GameMother:
    async def a_game(
        self,
        num_slots: int,
        num_colors: int,
        max_guesses: int,
        secret_code: list[Color],
        reference: str | None = None,
    ) -> Game:
        async with provide(MongoUnitOfWork) as uow:
            game = Game.new(
                id=uow.games.next_id(),
                num_slots=num_slots,
                num_colors=num_colors,
                max_guesses=max_guesses,
            )
            game.secret_code = secret_code

            if reference:
                game.reference = reference

            await uow.games.asave(game)
            await uow.commit()
        return game

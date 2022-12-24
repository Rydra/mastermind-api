import uuid

from apps.mastermind.core.domain.domain import Game, Guess
from apps.mastermind.core.domain.interfaces import IGameRepository
from apps.mastermind.infrastructure.persistence.models import GameModel, GuessModel
from apps.shared.typing import Id


class GameRepository(IGameRepository):
    def all(self) -> list[Game]:
        models = GameModel.objects.all()
        return [self._to_domain(model) for model in models]

    async def count(self) -> int:
        return await GameModel.objects.count()

    def save(self, game: Game) -> None:
        model = self._to_model(game)

        model.save()

        GuessModel.objects.filter(game_id=model.id).delete()

        for g in game.guesses:
            GuessModel.objects.create(
                code=g.code,
                black_pegs=g.black_pegs,
                white_pegs=g.white_pegs,
                game_id=model.id,
            )

        game.id = model.id

    def next_id(self) -> Id:
        return str(uuid.uuid4())

    def get(self, id: int) -> Game:
        return self._to_domain(GameModel.objects.get(pk=id))

    def _to_domain(self, model: GameModel) -> Game:
        guesses = [
            Guess(g.code, g.black_pegs, g.white_pegs)
            for g in model.guesses.order_by("timestamp")
        ]

        return Game(
            id=model.id,
            reference=model.reference,
            num_colors=model.num_colors,
            num_slots=model.num_slots,
            max_guesses=model.max_guesses,
            status=model.status,
            secret_code=model.secret_code,
            guesses=guesses,
        )

    def _to_model(self, game: Game) -> GameModel:
        model = GameModel(
            id=game.id,
            reference=game.reference,
            num_colors=game.num_colors,
            num_slots=game.num_slots,
            max_guesses=game.max_guesses,
            status=game.status,
            secret_code=game.secret_code,
        )

        return model

    async def aall(self) -> list[Game]:
        models = GameModel.objects.all()
        return [await self._ato_domain(model) async for model in models]

    async def asave(self, game: Game) -> None:
        if not game.id:
            game_model = await GameModel.objects.acreate(
                reference=game.reference,
                num_colors=game.num_colors,
                num_slots=game.num_slots,
                max_guesses=game.max_guesses,
                status=game.status,
                secret_code=game.secret_code,
            )
            game.id = game_model.id
        else:
            await GameModel.objects.aupdate_or_create(
                id=game.id,
                defaults=dict(
                    reference=game.reference,
                    num_colors=game.num_colors,
                    num_slots=game.num_slots,
                    max_guesses=game.max_guesses,
                    status=game.status,
                    secret_code=game.secret_code,
                ),
            )

        await GuessModel.objects.filter(game_id=game.id).adelete()

        for g in game.guesses:
            await GuessModel.objects.acreate(
                code=g.code,
                black_pegs=g.black_pegs,
                white_pegs=g.white_pegs,
                game_id=game.id,
            )

    async def aget(self, id: int) -> Game:
        return await self._ato_domain(await GameModel.objects.aget(pk=id))

    async def _ato_domain(self, model: GameModel) -> Game:
        guesses = [
            Guess(g.code, g.black_pegs, g.white_pegs)
            async for g in model.guesses.order_by("timestamp")
        ]

        return Game(
            id=model.id,
            reference=model.reference,
            num_colors=model.num_colors,
            num_slots=model.num_slots,
            max_guesses=model.max_guesses,
            status=model.status,
            secret_code=model.secret_code,
            guesses=guesses,
        )

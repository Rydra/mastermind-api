from typing import List

from bson import ObjectId
from pymongo import MongoClient

from apps.mastermind.core.domain.domain import Game, Guess
from apps.mastermind.core.domain.interfaces import IGameRepository
from apps.shared.typing import Id


class MongoGameRepository(IGameRepository):
    def __init__(self, client: MongoClient) -> None:
        self.client = client
        self.mastermind_db = self.client.mastermind_db
        self.game_collection = self.mastermind_db.game_collection

    def all(self) -> list[Game]:
        return []

    def save(self, game: Game) -> None:
        pass

    def get(self, id: int) -> Game:
        pass

    async def aall(self) -> List[Game]:
        return [self._to_domain(d) async for d in self.game_collection.find()]

    async def asave(self, game: Game) -> None:
        game_dict = {
            "reference": game.reference,
            "num_slots": game.num_slots,
            "num_colors": game.num_colors,
            "secret_code": game.secret_code,
            "max_guesses": game.max_guesses,
            "status": game.status,
            "guesses": [
                {
                    "code": guess.code,
                    "black_pegs": guess.black_pegs,
                    "white_pegs": guess.white_pegs,
                }
                for guess in game.guesses
            ],
        }

        if not game.id:
            game_id = (await self.game_collection.insert_one(game_dict)).inserted_id
            game.id = str(game_id)
        else:
            await self.game_collection.replace_one(
                {"_id": ObjectId(game.id)}, game_dict, upsert=True
            )

    async def aget(self, id: Id) -> Game:
        document = await self.game_collection.find_one({"_id": ObjectId(id)})
        if not document:
            raise Exception("Not found")

        return self._to_domain(document)

    def _to_domain(self, document: dict) -> Game:
        return Game(
            id=str(document["_id"]),
            reference=document["reference"],
            num_slots=document["num_slots"],
            num_colors=document["num_colors"],
            secret_code=document["secret_code"],
            max_guesses=document["max_guesses"],
            status=document["status"],
            guesses=[
                Guess(
                    code=guess["code"],
                    black_pegs=guess["black_pegs"],
                    white_pegs=guess["white_pegs"],
                )
                for guess in document["guesses"]
            ],
        )

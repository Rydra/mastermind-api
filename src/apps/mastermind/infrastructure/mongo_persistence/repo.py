import logging

from bson import ObjectId
from bson.errors import InvalidId
from motor.core import AgnosticDatabase
from pymongo import InsertOne, ReplaceOne

from apps.mastermind.core.domain.domain import Game, Guess
from apps.mastermind.core.domain.interfaces import IGameRepository
from apps.mastermind.infrastructure.mongo_persistence.session import Session
from apps.shared.exceptions import NotFound
from apps.shared.typing import Id

logger = logging.getLogger()


class MongoGameRepository(IGameRepository):
    def __init__(self, database: AgnosticDatabase, session: Session) -> None:
        self.session = session
        self.game_collection = database.game_collection

    async def aall(self) -> list[Game]:
        return [self._to_domain(d) async for d in self.game_collection.find()]

    def next_id(self) -> Id:
        return str(ObjectId())

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
            self.session.add_operation(self.game_collection, InsertOne(game_dict))
        else:
            self.session.add_operation(
                self.game_collection,
                ReplaceOne({"_id": ObjectId(game.id)}, game_dict, upsert=True),
            )

    async def count(self) -> int:
        return await self.game_collection.count_documents({})

    async def aget(self, id: Id) -> Game:
        try:
            document = await self.game_collection.find_one({"_id": ObjectId(id)})
        except InvalidId:
            document = None

        if not document:
            raise NotFound()

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

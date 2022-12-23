from fastapi import APIRouter
from fastapi_utils.cbv import cbv
from starlette.responses import JSONResponse

from apps.mastermind.core.commands.game import CreateGame, AddGuess
from apps.mastermind.core.queries.game import (
    ListGamesHandler,
    ListGames,
    GetGameHandler,
    GetGame,
)
from apps.mastermind.infrastructure.api.dtos import (
    GameDto,
    ListGamesResponse,
    AddGuessRequest,
    CreateGameRequest,
)
from apps.shared.command_bus import CommandBus
from apps.shared.message import Message
from composite_root.container import provide

router = APIRouter(tags=["Game"], prefix="")


@cbv(router)
class GameController:
    @router.get(
        "/api/games/",
        summary="Get all the games",
        responses={
            400: {
                "model": Message,
                "description": "Bad request. There are any error in parameters",
            },
            500: {"model": Message, "description": "Internal server error."},
        },
    )
    async def list_games(self) -> ListGamesResponse:
        try:
            games = await provide(ListGamesHandler).run(ListGames())
            results = ListGamesResponse(
                results=[GameDto.from_domain(game) for game in games]
            )
            return results
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=500)

    @router.get(
        "/api/games/{game_id}/",
        summary="Get a game by ID",
        responses={
            400: {
                "model": Message,
                "description": "Bad request. There are any error in parameters",
            },
            500: {"model": Message, "description": "Internal server error."},
        },
    )
    async def get_game(self, game_id: int) -> GameDto:
        try:
            game = await provide(GetGameHandler).run(GetGame(id=game_id))
            return GameDto.from_domain(game)
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=500)

    @router.post(
        "/api/games/",
        summary="Create a new game",
        status_code=201,
        responses={
            400: {
                "model": Message,
                "description": "Bad request. There are any error in parameters",
            },
            500: {"model": Message, "description": "Internal server error."},
        },
    )
    async def create_game(self, request: CreateGameRequest) -> GameDto:
        try:
            command = CreateGame(
                num_slots=request.num_slots,
                num_colors=request.num_colors,
                max_guesses=request.max_guesses,
            )
            game = await CommandBus().asend(command)

            return GameDto.from_domain(game)
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=500)

    @router.post(
        "/api/games/{game_id}/guesses/",
        summary="Add a new guess to a game",
        responses={
            400: {
                "model": Message,
                "description": "Bad request. There are any error in parameters",
            },
            500: {"model": Message, "description": "Internal server error."},
        },
    )
    async def add_guess(self, game_id: int, request: AddGuessRequest) -> GameDto:
        try:
            game = await CommandBus().asend(AddGuess(id=game_id, code=request.code))

            return GameDto.from_domain(game)
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=500)

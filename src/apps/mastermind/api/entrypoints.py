from typing import Any

from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.shared.command_bus import CommandBus
from apps.mastermind.core.commands.game import (
    CreateGame,
    AddGuess,
)
from apps.mastermind.core.queries.game import (
    ListGames,
    ListGamesHandler,
    GetGameHandler,
    GetGame,
)
from apps.mastermind.api.dtos import GameSchema
from composite_root.container import provide


class MastermindViewset(viewsets.ViewSet):
    def list(self, request: Any) -> HttpResponse:
        games = provide(ListGamesHandler).run(ListGames())
        data = GameSchema(many=True).dump(games)
        return Response(data={"results": data})

    def create(self, request: Any) -> HttpResponse:
        command = CreateGame(**request.data)
        game = CommandBus().send(command)

        result = GameSchema().dump(game)

        return Response(status=status.HTTP_201_CREATED, data=result)

    def retrieve(self, request: Any, id: int) -> HttpResponse:
        game = provide(GetGameHandler).run(GetGame(id=id))
        data = GameSchema().dump(game)
        return Response(data=data)


class GuessesViewset(viewsets.ViewSet):
    def create(self, request: Any, id: int) -> HttpResponse:
        game = CommandBus().send(AddGuess(id=id, **request.data))
        result = GameSchema().dump(game)

        return Response(status=status.HTTP_201_CREATED, data=result)

import strawberry

from apps.mastermind.core.domain.domain import Color, GameState

ColorEnum = strawberry.enum(Color)
GameStateEnum = strawberry.enum(GameState)

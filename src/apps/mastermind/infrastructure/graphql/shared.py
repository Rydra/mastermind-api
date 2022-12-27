import strawberry

from apps.mastermind.core.domain.domain import Color

ColorNode = strawberry.enum(Color)

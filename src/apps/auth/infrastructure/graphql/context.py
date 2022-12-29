from typing import Any

from strawberry import BasePermission
from strawberry.fastapi import BaseContext
from strawberry.types import Info as _Info
from strawberry.types.info import RootValueType

from apps.auth.core.domain import User
from apps.auth.core.login_handlers import LoginHandler
from composite_root.container import provide
from config.settings import settings


class Context(BaseContext):
    def __init__(self) -> None:
        super().__init__()
        self._user: User | None = None

    async def user(self) -> User | None:
        if not self.request:
            return None

        if not self._user:

            authorization = self.request.headers.get("Authorization", None)
            user = await provide(LoginHandler).login_by_token(authorization)
            if not user or user.disabled:
                return None
            self._user = user

        return self._user


Info = _Info[Context, RootValueType]


class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    async def has_permission(self, source: Any, info: Info, **kwargs: Any) -> bool:
        if settings.ignore_authentication:
            return True

        user = await info.context.user()
        return bool(user)

from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError

from apps.auth.core.domain import User
from apps.auth.core.interfaces import IUserRepository, ITokenProvider
from composite_root.container import provide


class ILoginHandler:
    async def login_by_token(self, token: str) -> User:
        ...


class LoginHandler(ILoginHandler):
    def __init__(self) -> None:
        self.strategies = [provide(JWTLoginHandler), provide(ApiKeyLoginHandler)]

    async def login_by_token(self, token: str | None) -> User | None:
        user: User | None = None
        for strategy in self.strategies:
            user = await strategy.login_by_token(token)
            if user:
                break

        return user


class JWTLoginHandler(ILoginHandler):
    def __init__(
        self, user_repository: IUserRepository, token_provider: ITokenProvider
    ) -> None:
        self.user_repository = user_repository
        self.token_provider = token_provider

    async def login_by_token(self, token: str | None) -> User | None:
        scheme, token = get_authorization_scheme_param(token)
        if not token or scheme.lower() != "bearer":
            return None

        if not token:
            return None

        try:
            payload = await self.token_provider.decode_token(token)
        except JWTError:
            return None

        return await self._get_user_from_token_payload(payload, token)

    async def _get_user_from_token_payload(
        self, payload: dict, token: str
    ) -> User | None:
        username: str | None = payload.get("sub")
        return await self.user_repository.get_by_username(username)


class ApiKeyLoginHandler(ILoginHandler):
    def __init__(self, user_repository: IUserRepository) -> None:
        self.user_repository = user_repository

    async def login_by_token(self, token: str | None) -> User | None:
        scheme, token = get_authorization_scheme_param(token)
        if not token or scheme.lower() != "apikey":
            return None

        if token == "aaaaa":
            return await self.user_repository.get_by_username("john.doe")

        return None

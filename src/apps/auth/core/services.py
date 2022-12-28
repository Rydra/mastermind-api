from passlib.context import CryptContext

from apps.auth.core.domain import User
from apps.auth.core.interfaces import IUserRepository, ITokenProvider

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Authenticator:
    def __init__(
        self, user_repository: IUserRepository, token_provider: ITokenProvider
    ) -> None:
        self.user_repository = user_repository
        self.token_provider = token_provider

    async def authenticate(self, username: str, password: str) -> User | None:
        user = await self.user_repository.get_by_username(username)
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user

    def make_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    async def authenticate_by_token(self, token: str) -> User:
        payload = await self.token_provider.get_payload(token)
        return await self._get_user_from_token_payload(payload, token)

    async def _get_user_from_token_payload(
        self, payload: dict, token: str
    ) -> User | None:
        username: str | None = payload.get("sub")
        return await self.user_repository.get_by_username(username)

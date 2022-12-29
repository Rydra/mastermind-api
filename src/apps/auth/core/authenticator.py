from passlib.context import CryptContext

from apps.auth.core.domain import User
from apps.auth.core.interfaces import IUserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Authenticator:
    def __init__(self, user_repository: IUserRepository) -> None:
        self.user_repository = user_repository

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

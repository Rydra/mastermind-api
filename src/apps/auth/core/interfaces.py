from abc import ABC, abstractmethod
from typing import Any

from apps.auth.core.domain import User
from apps.shared.typing import Id


class ITokenProvider(ABC):
    @abstractmethod
    async def get_payload(self, token: str) -> dict:
        ...

    @abstractmethod
    async def create_token(self, data: dict, **kwargs: Any) -> str:
        ...


class ISecretProvider(ABC):
    @abstractmethod
    async def get_secret_key(self) -> str:
        ...


class IUserRepository(ABC):
    @abstractmethod
    async def get(self, id: Id) -> User | None:
        ...

    @abstractmethod
    async def get_by_username(self, username: str) -> User | None:
        ...

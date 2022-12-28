from datetime import timedelta, datetime
from typing import Any

from apps.auth.core.interfaces import ITokenProvider, ISecretProvider
from jose import jwt

from config.settings import settings


class JWTTokenProvider(ITokenProvider):
    def __init__(self, secret_provider: ISecretProvider) -> None:
        self.secret_provider = secret_provider

    async def get_payload(self, token: str) -> dict:
        payload = jwt.decode(
            token,
            await self.secret_provider.get_secret_key(),
            algorithms=[settings.algorithm],
        )
        return payload

    async def encode_payload(
        self, data: dict, expires_delta: timedelta | None = None, **kwargs: Any
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        secret_key = await self.secret_provider.get_secret_key()
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=settings.algorithm)
        return encoded_jwt

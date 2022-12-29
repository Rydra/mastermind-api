from datetime import timedelta

import strawberry
from strawberry import ID

from apps.auth.core.authenticator import Authenticator
from apps.auth.infrastructure.jwt import JWTTokenProvider
from composite_root.container import provide
from config.settings import settings


@strawberry.type
class LoginSuccess:
    access_token: str
    username: str
    user_id: ID
    token_type: str


@strawberry.type
class LoginError:
    message: str


LoginResult = strawberry.union("LoginResult", (LoginSuccess, LoginError))


@strawberry.type
class AuthMutations:
    @strawberry.mutation
    async def login(self, username: str, password: str) -> LoginResult:
        user = await provide(Authenticator).authenticate(username, password)
        if not user:
            return LoginError(message="Invalid user or password")

        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = await provide(JWTTokenProvider).create_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return LoginSuccess(
            access_token=access_token,
            username=user.username,
            user_id=user.id,
            token_type="bearer",
        )

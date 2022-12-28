from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_utils.cbv import cbv
from starlette import status
from jose import JWTError

from apps.auth.core.domain import User
from apps.auth.core.services import Authenticator
from apps.auth.infrastructure.api.dtos import Token
from apps.auth.infrastructure.jwt import JWTTokenProvider
from composite_root.container import provide
from config.settings import settings

router = APIRouter(tags=["Auth"], prefix="")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        user = await provide(Authenticator).authenticate_by_token(token)
    except JWTError:
        raise credentials_exception

    if not user:
        raise credentials_exception

    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return user


@cbv(router)
class AuthController:
    @router.post(
        "/token",
        summary="Obtains a new token for a logged in user",
        response_model=Token,
    )
    async def new_token(
        self, form_data: OAuth2PasswordRequestForm = Depends()
    ) -> Token:
        user = await provide(Authenticator).authenticate(
            form_data.username, form_data.password
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = await provide(JWTTokenProvider).encode_payload(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

from typing import Callable

import pinject

from apps.auth.infrastructure.jwt import JWTTokenProvider
from apps.auth.infrastructure.persistence.repo import UserRepository
from apps.auth.infrastructure.secret_providers import LocalSecretProvider


class AuthBindingSpec(pinject.BindingSpec):
    def configure(self, bind: Callable) -> None:
        bind("user_repository", to_class=UserRepository)
        bind("token_provider", to_class=JWTTokenProvider)
        bind("secret_provider", to_class=LocalSecretProvider)

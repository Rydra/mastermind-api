from apps.auth.core.interfaces import ISecretProvider
from config.settings import settings


class LocalSecretProvider(ISecretProvider):
    async def get_secret_key(self) -> str:
        return settings.secret_key

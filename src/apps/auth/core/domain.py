from pydantic import BaseModel

from apps.shared.typing import Id


class User(BaseModel):
    id: Id
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    hashed_password: str

from typing import TypeAlias, TypeVar
from uuid import UUID

Id: TypeAlias = int | str | UUID
T = TypeVar("T")

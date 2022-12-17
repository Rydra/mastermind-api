from abc import abstractmethod, ABC
from typing import Any

from pydantic import BaseModel


class Command(BaseModel):
    pass


class Query(BaseModel):
    pass


class CommandHandler(ABC):
    @abstractmethod
    def run(self, command: Command) -> Any:
        pass

from collections import defaultdict
from typing import Any

from motor.core import AgnosticCollection

from apps.shared.uow import BaseSession


class Session(BaseSession):
    def __init__(self) -> None:
        super().__init__()
        self.operations: dict = defaultdict(list)

    def add_operation(self, collection: AgnosticCollection, operation: Any) -> None:
        self.operations[collection].append(operation)

    async def _commit(self) -> None:
        for collection, operations in self.operations.items():
            await collection.bulk_write(operations)

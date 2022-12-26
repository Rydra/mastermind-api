from typing import Any, Callable, List

import anyio
from anyio import start_blocking_portal


class NotYet(RuntimeError):
    pass


class ResultGatheringTaskgroup:
    def __init__(self) -> None:
        self.result: List = []

    async def __aenter__(self) -> "ResultGatheringTaskgroup":
        self._taskgroup = tg = anyio.create_task_group()
        await tg.__aenter__()
        return self

    async def __aexit__(self, *tb: Any) -> Any:
        try:
            res = await self._taskgroup.__aexit__(*tb)
            return res
        finally:
            del self._taskgroup

    async def _run_one(self, pos: int, proc: Callable, a: Any) -> None:
        self.result[pos] = await proc(*a)

    def start_soon(self, proc: Callable, *a: Any) -> int:
        pos = len(self.result)
        self.result.append(NotYet)
        self._taskgroup.start_soon(self._run_one, pos, proc, a)
        return pos

    def get_result(self, pos: int) -> Any:
        res = self.result[pos]
        if res is NotYet:
            raise NotYet()
        return res


def async_to_sync(f: Callable, *args: Any, **kwargs: Any) -> Any:
    """
    This version of the async_to_sync, compared with the one of asgiref,
    is more pytest-friendly and does not cause failures
    """
    with start_blocking_portal() as portal:
        return portal.call(f, *args, **kwargs)

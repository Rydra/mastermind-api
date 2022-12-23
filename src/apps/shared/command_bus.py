import inspect
from typing import Any

from singleton import Singleton

from apps.shared.interfaces import CommandHandler, Command


class CommandBus(metaclass=Singleton):
    # TODO: For now let's make the command bus synchronous. In the future
    # we should make this async, as it is more conventional for regular
    # CQRS architectures
    def __init__(self) -> None:
        self.handlers: dict[type[Command], CommandHandler] = {}

    def register_handler(self, handler: CommandHandler) -> None:
        for param_name, type in inspect.signature(handler.run).parameters.items():
            if param_name == "command":
                self.handlers[type.annotation] = handler

    def reset(self) -> None:
        self.handlers.clear()

    def send(self, command: Command) -> Any:
        handler = self.handlers.get(type(command))
        if handler:
            return handler.run(command)

    async def asend(self, command: Command) -> Any:
        handler = self.handlers.get(type(command))
        if handler:
            if inspect.iscoroutinefunction(handler.run):
                return await handler.run(command)
            return handler.run(command)

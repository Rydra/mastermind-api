from apps.infrastructure.command_bus import CommandBus
from apps.mastermind.commands.game import CreateGameHandler, AddGuessHandler
from config.composite_root.container import provide


def bootstrap() -> None:
    for handler in [CreateGameHandler, AddGuessHandler]:
        CommandBus().register_handler(provide(handler))

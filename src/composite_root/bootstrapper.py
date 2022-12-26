from apps.shared.cache import init_cache
from apps.shared.command_bus import CommandBus
from apps.mastermind.core.commands.game import CreateGameHandler, AddGuessHandler
from composite_root.container import provide


def bootstrap() -> None:
    init_cache()

    for handler in [CreateGameHandler, AddGuessHandler]:
        CommandBus().register_handler(provide(handler))

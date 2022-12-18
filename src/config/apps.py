from django.apps import AppConfig


class MastermindConfig(AppConfig):
    """
    Put any initialization code (or code that must run once) in the ready method of this class
    """

    name = "config"

    def ready(self) -> None:
        from composite_root.bootstrapper import bootstrap

        bootstrap()

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MastermindConfig(AppConfig):
    name = "apps.mastermind.persistence"
    label = "mastermind"
    verbose_name = _("Mastermind")

from pathlib import Path

from split_settings.tools import include


from decouple import config as config_dec
from pysettings_yaml import get_config
from split_settings.tools import optional

ENVIRONMENT = config_dec("ENVIRONMENT", default="dev")

SETTINGS_DIR = Path(__file__).parent
setting_files = [
    SETTINGS_DIR / "settings.yaml",
    optional(SETTINGS_DIR / f"settings.{ENVIRONMENT}.yaml"),
]

config = get_config(setting_files)

include("base.py", "local.py")

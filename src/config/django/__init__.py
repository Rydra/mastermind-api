from split_settings.tools import include

from config.settings import Settings

settings = Settings()
ENVIRONMENT = settings.env

include("base.py", "local.py")

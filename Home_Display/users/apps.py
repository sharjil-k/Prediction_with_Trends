from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "Home_Display.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import Home_Display.users.signals  # noqa F401
        except ImportError:
            pass

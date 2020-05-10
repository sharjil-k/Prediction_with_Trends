from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class HomeDisplayConfig(AppConfig):
    name = 'Home_Display'


class UsersConfig(AppConfig):
    name = "Home_Display.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import pset_6.users.signals  # noqa F401
        except ImportError:
            pass
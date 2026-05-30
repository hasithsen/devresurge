from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProfilesConfig(AppConfig):
    name = "devresurge.profiles"
    verbose_name = _("Profiles")
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self) -> None:
        # Connect post_save signal that auto-creates a Profile per User.
        from . import signals  # noqa: F401, PLC0415

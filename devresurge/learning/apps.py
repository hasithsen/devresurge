from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LearningConfig(AppConfig):
    name = "devresurge.learning"
    verbose_name = _("Learning")
    default_auto_field = "django.db.models.BigAutoField"

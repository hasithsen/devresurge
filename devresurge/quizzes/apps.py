from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class QuizzesConfig(AppConfig):
    name = "devresurge.quizzes"
    verbose_name = _("Quizzes")
    default_auto_field = "django.db.models.BigAutoField"

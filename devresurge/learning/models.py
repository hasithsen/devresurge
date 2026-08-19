from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class LessonProgress(models.Model):
    """Per-user progress through a catalog lesson (quest)."""

    class Status(models.TextChoices):
        STARTED = "started", _("Started")
        COMPLETED = "completed", _("Completed")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lesson_progress",
    )
    roadmap_slug = models.SlugField(_("roadmap"), max_length=80)
    lesson_slug = models.SlugField(_("lesson"), max_length=80)
    status = models.CharField(
        _("status"),
        max_length=12,
        choices=Status.choices,
        default=Status.STARTED,
    )
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated_at",)
        verbose_name = _("lesson progress")
        verbose_name_plural = _("lesson progress")
        constraints = [
            models.UniqueConstraint(
                fields=("user", "roadmap_slug", "lesson_slug"),
                name="learning_progress_user_lesson_uniq",
            ),
        ]
        indexes = [
            models.Index(
                fields=["user", "roadmap_slug"],
                name="learning_prog_user_rm_idx",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.user_id} · {self.roadmap_slug}/{self.lesson_slug}"

    @property
    def is_completed(self) -> bool:
        return self.status == self.Status.COMPLETED

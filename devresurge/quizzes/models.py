from __future__ import annotations

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Quiz(models.Model):
    """A short skill check that awards a badge on pass."""

    slug = models.SlugField(_("slug"), max_length=60, unique=True)
    title = models.CharField(_("title"), max_length=120)
    tagline = models.CharField(_("tagline"), max_length=200, blank=True)
    description = models.TextField(_("description"), blank=True)
    topic = models.CharField(
        _("topic"),
        max_length=40,
        blank=True,
        help_text=_("e.g. python, git, django"),
    )
    pass_percent = models.PositiveSmallIntegerField(
        _("pass percent"),
        default=80,
        help_text=_("Score required to pass (0–100)."),
    )
    badge_slug = models.SlugField(
        _("badge slug"),
        max_length=60,
        blank=True,
        help_text=_("Achievement badge awarded on first pass."),
    )
    is_published = models.BooleanField(_("published"), default=True)
    order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("order", "title")
        verbose_name = _("quiz")
        verbose_name_plural = _("quizzes")

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("quizzes:detail", kwargs={"slug": self.slug})

    @property
    def question_count(self) -> int:
        return self.questions.count()


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    prompt = models.TextField(_("prompt"))
    explanation = models.TextField(
        _("explanation"),
        blank=True,
        help_text=_("Shown after submit when the answer was wrong."),
    )
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("order", "pk")
        verbose_name = _("question")
        verbose_name_plural = _("questions")

    def __str__(self) -> str:
        return self.prompt[:60]


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="choices",
    )
    label = models.CharField(_("label"), max_length=300)
    is_correct = models.BooleanField(_("correct"), default=False)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("order", "pk")
        verbose_name = _("choice")
        verbose_name_plural = _("choices")

    def __str__(self) -> str:
        return self.label[:60]


class QuizAttempt(models.Model):
    """One completed attempt at a quiz by a user."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="quiz_attempts",
    )
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="attempts")
    score = models.PositiveSmallIntegerField(_("score"), default=0)
    total = models.PositiveSmallIntegerField(_("total"), default=0)
    percent = models.PositiveSmallIntegerField(_("percent"), default=0)
    passed = models.BooleanField(_("passed"), default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("quiz attempt")
        verbose_name_plural = _("quiz attempts")
        indexes = [
            models.Index(fields=["user", "quiz"], name="quizzes_attempt_user_quiz_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.user_id} @ {self.quiz_id}: {self.percent}%"


class BadgeCategory(models.TextChoices):
    PROFILE = "profile", _("Profile")
    NETWORK = "network", _("Network")
    QUIZ = "quiz", _("Quiz")
    MILESTONE = "milestone", _("Milestone")


class Badge(models.Model):
    """Catalog entry for an achievement shown on public profiles."""

    slug = models.SlugField(_("slug"), max_length=60, unique=True)
    title = models.CharField(_("title"), max_length=80)
    description = models.CharField(_("description"), max_length=200)
    icon = models.CharField(
        _("icon"),
        max_length=8,
        default="★",
        help_text=_("Single glyph shown in the badge chip."),
    )
    category = models.CharField(
        _("category"),
        max_length=20,
        choices=BadgeCategory.choices,
        default=BadgeCategory.MILESTONE,
    )
    is_active = models.BooleanField(_("active"), default=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("order", "title")
        verbose_name = _("badge")
        verbose_name_plural = _("badges")

    def __str__(self) -> str:
        return self.title


class UserBadge(models.Model):
    """A badge earned by a user (via their profile)."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="badges",
    )
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name="awards")
    earned_at = models.DateTimeField(default=timezone.now, db_index=True)
    # Optional: which quiz attempt unlocked a quiz badge.
    quiz_attempt = models.ForeignKey(
        QuizAttempt,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="badges_awarded",
    )

    class Meta:
        ordering = ("-earned_at",)
        verbose_name = _("user badge")
        verbose_name_plural = _("user badges")
        constraints = [
            models.UniqueConstraint(
                fields=("user", "badge"),
                name="quizzes_userbadge_unique",
            ),
        ]
        indexes = [
            models.Index(fields=["user", "earned_at"], name="quizzes_ub_user_earned_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.user_id} · {self.badge_id}"

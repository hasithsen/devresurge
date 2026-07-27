# Generated manually for quizzes + badges

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations
from django.db import models


def seed_forward(apps, schema_editor):  # noqa: ARG001
    from devresurge.quizzes.catalog import seed_catalog

    seed_catalog(refresh_questions=True)


def seed_reverse(apps, schema_editor):  # noqa: ARG001
    Quiz = apps.get_model("quizzes", "Quiz")
    Badge = apps.get_model("quizzes", "Badge")
    Quiz.objects.filter(
        slug__in=["python-fundamentals", "git-collaboration", "django-basics"],
    ).delete()
    Badge.objects.filter(
        slug__in=[
            "profile_ready",
            "open_to_work",
            "shipper",
            "first_link",
            "networker",
            "quiz_python",
            "quiz_git",
            "quiz_django",
            "quiz_streak",
        ],
    ).delete()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Badge",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("slug", models.SlugField(max_length=60, unique=True, verbose_name="slug")),
                ("title", models.CharField(max_length=80, verbose_name="title")),
                ("description", models.CharField(max_length=200, verbose_name="description")),
                (
                    "icon",
                    models.CharField(
                        default="★",
                        help_text="Single glyph shown in the badge chip.",
                        max_length=8,
                        verbose_name="icon",
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("profile", "Profile"),
                            ("network", "Network"),
                            ("quiz", "Quiz"),
                            ("milestone", "Milestone"),
                        ],
                        default="milestone",
                        max_length=20,
                        verbose_name="category",
                    ),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="active")),
                ("order", models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                "verbose_name": "badge",
                "verbose_name_plural": "badges",
                "ordering": ("order", "title"),
            },
        ),
        migrations.CreateModel(
            name="Quiz",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("slug", models.SlugField(max_length=60, unique=True, verbose_name="slug")),
                ("title", models.CharField(max_length=120, verbose_name="title")),
                ("tagline", models.CharField(blank=True, max_length=200, verbose_name="tagline")),
                ("description", models.TextField(blank=True, verbose_name="description")),
                (
                    "topic",
                    models.CharField(
                        blank=True,
                        help_text="e.g. python, git, django",
                        max_length=40,
                        verbose_name="topic",
                    ),
                ),
                (
                    "pass_percent",
                    models.PositiveSmallIntegerField(
                        default=80,
                        help_text="Score required to pass (0–100).",
                        verbose_name="pass percent",
                    ),
                ),
                (
                    "badge_slug",
                    models.SlugField(
                        blank=True,
                        help_text="Achievement badge awarded on first pass.",
                        max_length=60,
                        verbose_name="badge slug",
                    ),
                ),
                ("is_published", models.BooleanField(default=True, verbose_name="published")),
                ("order", models.PositiveSmallIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "quiz",
                "verbose_name_plural": "quizzes",
                "ordering": ("order", "title"),
            },
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("prompt", models.TextField(verbose_name="prompt")),
                (
                    "explanation",
                    models.TextField(
                        blank=True,
                        help_text="Shown after submit when the answer was wrong.",
                        verbose_name="explanation",
                    ),
                ),
                ("order", models.PositiveSmallIntegerField(default=0)),
                (
                    "quiz",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="questions",
                        to="quizzes.quiz",
                    ),
                ),
            ],
            options={
                "verbose_name": "question",
                "verbose_name_plural": "questions",
                "ordering": ("order", "pk"),
            },
        ),
        migrations.CreateModel(
            name="Choice",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("label", models.CharField(max_length=300, verbose_name="label")),
                ("is_correct", models.BooleanField(default=False, verbose_name="correct")),
                ("order", models.PositiveSmallIntegerField(default=0)),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="choices",
                        to="quizzes.question",
                    ),
                ),
            ],
            options={
                "verbose_name": "choice",
                "verbose_name_plural": "choices",
                "ordering": ("order", "pk"),
            },
        ),
        migrations.CreateModel(
            name="QuizAttempt",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("score", models.PositiveSmallIntegerField(default=0, verbose_name="score")),
                ("total", models.PositiveSmallIntegerField(default=0, verbose_name="total")),
                ("percent", models.PositiveSmallIntegerField(default=0, verbose_name="percent")),
                ("passed", models.BooleanField(default=False, verbose_name="passed")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "quiz",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attempts",
                        to="quizzes.quiz",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="quiz_attempts",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "quiz attempt",
                "verbose_name_plural": "quiz attempts",
                "ordering": ("-created_at",),
            },
        ),
        migrations.CreateModel(
            name="UserBadge",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "earned_at",
                    models.DateTimeField(db_index=True, default=django.utils.timezone.now),
                ),
                (
                    "badge",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="awards",
                        to="quizzes.badge",
                    ),
                ),
                (
                    "quiz_attempt",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="badges_awarded",
                        to="quizzes.quizattempt",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="badges",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "user badge",
                "verbose_name_plural": "user badges",
                "ordering": ("-earned_at",),
            },
        ),
        migrations.AddIndex(
            model_name="quizattempt",
            index=models.Index(
                fields=["user", "quiz"],
                name="quizzes_attempt_user_quiz_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="userbadge",
            index=models.Index(
                fields=["user", "earned_at"],
                name="quizzes_ub_user_earned_idx",
            ),
        ),
        migrations.AddConstraint(
            model_name="userbadge",
            constraint=models.UniqueConstraint(
                fields=("user", "badge"),
                name="quizzes_userbadge_unique",
            ),
        ),
        migrations.RunPython(seed_forward, seed_reverse),
    ]

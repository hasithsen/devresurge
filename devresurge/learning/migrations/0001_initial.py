from django.conf import settings
from django.db import migrations
from django.db import models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="LessonProgress",
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
                ("roadmap_slug", models.SlugField(max_length=80, verbose_name="roadmap")),
                ("lesson_slug", models.SlugField(max_length=80, verbose_name="lesson")),
                (
                    "status",
                    models.CharField(
                        choices=[("started", "Started"), ("completed", "Completed")],
                        default="started",
                        max_length=12,
                        verbose_name="status",
                    ),
                ),
                ("started_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("completed_at", models.DateTimeField(blank=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lesson_progress",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "lesson progress",
                "verbose_name_plural": "lesson progress",
                "ordering": ("-updated_at",),
            },
        ),
        migrations.AddConstraint(
            model_name="lessonprogress",
            constraint=models.UniqueConstraint(
                fields=("user", "roadmap_slug", "lesson_slug"),
                name="learning_progress_user_lesson_uniq",
            ),
        ),
        migrations.AddIndex(
            model_name="lessonprogress",
            index=models.Index(
                fields=["user", "roadmap_slug"],
                name="learning_prog_user_rm_idx",
            ),
        ),
    ]

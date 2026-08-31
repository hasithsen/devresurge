# Profile tools showcase (daily drivers by field)

import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0010_alter_showcaseitem_excalidraw_png"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProfileTool",
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
                ("name", models.CharField(max_length=80, verbose_name="name")),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("languages", "Languages"),
                            ("frameworks", "Frameworks & libraries"),
                            ("infra", "Infra & cloud"),
                            ("data", "Data & analytics"),
                            ("observability", "Observability"),
                            ("security", "Security"),
                            ("collab", "Collaboration"),
                            ("design", "Design"),
                            ("ai", "AI / ML"),
                            ("other", "Other"),
                        ],
                        default="other",
                        max_length=24,
                        verbose_name="category",
                    ),
                ),
                (
                    "url",
                    models.URLField(
                        blank=True,
                        help_text="Optional docs or product page.",
                        max_length=300,
                        verbose_name="URL",
                    ),
                ),
                (
                    "note",
                    models.CharField(
                        blank=True,
                        help_text="How you use it — one short line.",
                        max_length=160,
                        verbose_name="note",
                    ),
                ),
                (
                    "is_featured",
                    models.BooleanField(default=False, verbose_name="featured"),
                ),
                ("order", models.PositiveSmallIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tools",
                        to="profiles.profile",
                    ),
                ),
            ],
            options={
                "verbose_name": "tool",
                "verbose_name_plural": "tools",
                "ordering": ("order", "name"),
            },
        ),
        migrations.AddConstraint(
            model_name="profiletool",
            constraint=models.UniqueConstraint(
                fields=("profile", "name"),
                name="profiles_profiletool_unique_name_per_profile",
            ),
        ),
    ]

# Generated manually for GitHub-backed profile showcases

import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0007_linkedin_complement"),
    ]

    operations = [
        migrations.CreateModel(
            name="ShowcaseItem",
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
                ("slug", models.SlugField(max_length=80)),
                ("title", models.CharField(max_length=140, verbose_name="title")),
                (
                    "summary",
                    models.CharField(
                        blank=True,
                        help_text="One line visitors see on your profile card.",
                        max_length=280,
                        verbose_name="summary",
                    ),
                ),
                (
                    "kind",
                    models.CharField(
                        choices=[
                            ("excalidraw", "Excalidraw system design"),
                            ("markdown", "Markdown notes"),
                            ("notes", "Plain / LFS-style notes"),
                            ("image", "Diagram / image"),
                        ],
                        default="markdown",
                        max_length=20,
                        verbose_name="kind",
                    ),
                ),
                (
                    "github_url",
                    models.URLField(
                        help_text=(
                            "Public file link, e.g. "
                            "https://github.com/you/repo/blob/main/designs/api.excalidraw"
                        ),
                        max_length=500,
                        verbose_name="GitHub file URL",
                    ),
                ),
                ("github_owner", models.CharField(blank=True, max_length=100)),
                ("github_repo", models.CharField(blank=True, max_length=100)),
                ("github_path", models.CharField(blank=True, max_length=400)),
                (
                    "github_ref",
                    models.CharField(blank=True, default="main", max_length=120),
                ),
                (
                    "tags",
                    models.CharField(
                        blank=True,
                        help_text="Comma-separated, e.g. 'system-design, excalidraw, linux'.",
                        max_length=240,
                        verbose_name="tags",
                    ),
                ),
                ("content_cache", models.TextField(blank=True)),
                ("preview_image_url", models.URLField(blank=True, max_length=500)),
                ("content_sha", models.CharField(blank=True, max_length=64)),
                ("fetched_at", models.DateTimeField(blank=True, null=True)),
                ("fetch_error", models.CharField(blank=True, max_length=240)),
                (
                    "is_featured",
                    models.BooleanField(default=False, verbose_name="featured"),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True,
                        help_text="Unpublish to hide from your public profile without deleting.",
                        verbose_name="published",
                    ),
                ),
                ("order", models.PositiveSmallIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="showcases",
                        to="profiles.profile",
                    ),
                ),
            ],
            options={
                "ordering": ("order", "-updated_at"),
            },
        ),
        migrations.AddConstraint(
            model_name="showcaseitem",
            constraint=models.UniqueConstraint(
                fields=("profile", "slug"),
                name="profiles_showcaseitem_unique_slug_per_profile",
            ),
        ),
    ]

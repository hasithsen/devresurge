# Generated manually for LinkedIn-complementary career signal

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0006_handle_case_insensitive"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="open_to_collaborate",
            field=models.BooleanField(
                default=False,
                help_text="Side projects, OSS, or consulting together.",
                verbose_name="open to collaborate",
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="open_to_learning",
            field=models.BooleanField(
                default=False,
                help_text="Looking for guidance from more senior folks.",
                verbose_name="seeking mentorship",
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="open_to_mentor",
            field=models.BooleanField(
                default=False,
                help_text="Happy to mentor others.",
                verbose_name="open to mentor",
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="open_to_note",
            field=models.CharField(
                blank=True,
                help_text="Optional one-liner for recruiters / collaborators.",
                max_length=200,
                verbose_name="open-to note",
            ),
        ),
        migrations.CreateModel(
            name="WorkExperience",
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
                ("title", models.CharField(max_length=120, verbose_name="title")),
                ("company", models.CharField(max_length=120, verbose_name="company")),
                ("location", models.CharField(blank=True, max_length=120, verbose_name="location")),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="What you shipped — Markdown-lite plain text is fine.",
                        verbose_name="description",
                    ),
                ),
                (
                    "start_year",
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1970),
                            django.core.validators.MaxValueValidator(2100),
                        ],
                        verbose_name="start year",
                    ),
                ),
                (
                    "start_month",
                    models.PositiveSmallIntegerField(
                        default=1,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(12),
                        ],
                        verbose_name="start month",
                    ),
                ),
                (
                    "end_year",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1970),
                            django.core.validators.MaxValueValidator(2100),
                        ],
                        verbose_name="end year",
                    ),
                ),
                (
                    "end_month",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(12),
                        ],
                        verbose_name="end month",
                    ),
                ),
                ("is_current", models.BooleanField(default=False, verbose_name="current role")),
                ("order", models.PositiveSmallIntegerField(default=0)),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="experiences",
                        to="profiles.profile",
                    ),
                ),
            ],
            options={
                "verbose_name": "work experience",
                "verbose_name_plural": "work experience",
                "ordering": ("order", "-start_year", "-start_month"),
            },
        ),
        migrations.CreateModel(
            name="Education",
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
                ("school", models.CharField(max_length=160, verbose_name="school")),
                (
                    "degree",
                    models.CharField(
                        blank=True,
                        help_text="e.g. BSc Computer Science, Bootcamp",
                        max_length=120,
                        verbose_name="degree",
                    ),
                ),
                (
                    "field",
                    models.CharField(blank=True, max_length=120, verbose_name="field of study"),
                ),
                (
                    "start_year",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1970),
                            django.core.validators.MaxValueValidator(2100),
                        ],
                        verbose_name="start year",
                    ),
                ),
                (
                    "end_year",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1970),
                            django.core.validators.MaxValueValidator(2100),
                        ],
                        verbose_name="end year",
                    ),
                ),
                ("order", models.PositiveSmallIntegerField(default=0)),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="education",
                        to="profiles.profile",
                    ),
                ),
            ],
            options={
                "verbose_name": "education",
                "verbose_name_plural": "education",
                "ordering": ("order", "-end_year", "-start_year"),
            },
        ),
        migrations.CreateModel(
            name="SkillEndorsement",
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
                ("skill", models.CharField(max_length=64, verbose_name="skill")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "endorser",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="endorsements_given",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="endorsements",
                        to="profiles.profile",
                    ),
                ),
            ],
            options={
                "verbose_name": "skill endorsement",
                "verbose_name_plural": "skill endorsements",
                "ordering": ("-created_at",),
            },
        ),
        migrations.CreateModel(
            name="Recommendation",
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
                    "relationship",
                    models.CharField(
                        blank=True,
                        help_text="e.g. Worked together at Acme, mentored on Django",
                        max_length=80,
                        verbose_name="relationship",
                    ),
                ),
                ("body", models.TextField(max_length=800, verbose_name="recommendation")),
                (
                    "is_public",
                    models.BooleanField(default=True, verbose_name="visible on profile"),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="recommendations_written",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="recommendations_received",
                        to="profiles.profile",
                    ),
                ),
            ],
            options={
                "verbose_name": "recommendation",
                "verbose_name_plural": "recommendations",
                "ordering": ("-created_at",),
            },
        ),
        migrations.AddConstraint(
            model_name="skillendorsement",
            constraint=models.UniqueConstraint(
                fields=("profile", "endorser", "skill"),
                name="profiles_endorsement_unique",
            ),
        ),
        migrations.AddIndex(
            model_name="skillendorsement",
            index=models.Index(
                fields=["profile", "skill"],
                name="profiles_endorse_skill_idx",
            ),
        ),
        migrations.AddConstraint(
            model_name="recommendation",
            constraint=models.UniqueConstraint(
                fields=("profile", "author"),
                name="profiles_recommendation_unique_author",
            ),
        ),
    ]

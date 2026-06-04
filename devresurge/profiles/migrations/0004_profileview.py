import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0003_alter_profile_available_for_hire"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProfileView",
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
                    "visitor_hash",
                    models.CharField(
                        db_index=True,
                        help_text="Salted SHA-256 of IP + user agent. Not reversible.",
                        max_length=64,
                        verbose_name="visitor hash",
                    ),
                ),
                (
                    "referrer",
                    models.CharField(
                        blank=True,
                        help_text="Host the visitor arrived from, e.g. 'news.ycombinator.com'.",
                        max_length=255,
                        verbose_name="referrer host",
                    ),
                ),
                (
                    "is_unique",
                    models.BooleanField(
                        default=False,
                        help_text="True if this visitor's first view of this profile that day.",
                        verbose_name="first view of day",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="views",
                        to="profiles.profile",
                    ),
                ),
            ],
            options={
                "verbose_name": "profile view",
                "verbose_name_plural": "profile views",
                "ordering": ("-created_at",),
            },
        ),
        migrations.AddIndex(
            model_name="profileview",
            index=models.Index(
                fields=["profile", "created_at"],
                name="profiles_pv_prof_created_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="profileview",
            index=models.Index(
                fields=["profile", "visitor_hash"],
                name="profiles_pv_prof_visitor_idx",
            ),
        ),
    ]

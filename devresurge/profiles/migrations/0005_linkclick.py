import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0004_profileview"),
    ]

    operations = [
        migrations.CreateModel(
            name="LinkClick",
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
                    "kind",
                    models.CharField(
                        choices=[
                            ("project", "Project"),
                            ("social", "Social"),
                            ("website", "Website"),
                            ("email", "Email"),
                        ],
                        max_length=20,
                        verbose_name="link kind",
                    ),
                ),
                (
                    "target_id",
                    models.PositiveBigIntegerField(
                        blank=True,
                        help_text="PK of the clicked ProjectLink/SocialLink, if applicable.",
                        null=True,
                        verbose_name="target id",
                    ),
                ),
                ("label", models.CharField(blank=True, max_length=160, verbose_name="label")),
                (
                    "destination",
                    models.CharField(
                        blank=True,
                        help_text="Host the click leads to, e.g. 'github.com'.",
                        max_length=255,
                        verbose_name="destination host",
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
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="link_clicks",
                        to="profiles.profile",
                    ),
                ),
            ],
            options={
                "verbose_name": "link click",
                "verbose_name_plural": "link clicks",
                "ordering": ("-created_at",),
            },
        ),
        migrations.AddIndex(
            model_name="linkclick",
            index=models.Index(fields=["profile", "created_at"], name="profiles_lc_prof_created_idx"),
        ),
        migrations.AddIndex(
            model_name="linkclick",
            index=models.Index(fields=["profile", "kind"], name="profiles_lc_prof_kind_idx"),
        ),
    ]

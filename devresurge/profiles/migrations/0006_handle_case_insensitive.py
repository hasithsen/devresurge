from django.db import migrations
from django.db import models
from django.db.models.functions import Lower

HANDLE_MAX_LENGTH = 40


def normalize_handles(apps, schema_editor):
    """Lowercase all existing handles, resolving case-fold collisions.

    The earliest profile (by creation) keeps the bare handle; later collisions
    get a numeric suffix, mirroring `Profile.ensure_handle`.
    """
    profile_model = apps.get_model("profiles", "Profile")
    taken: set[str] = set()
    for profile in profile_model.objects.all().order_by("created_at", "pk").iterator():
        base = (profile.handle or "").strip().lower()
        if not base:
            continue
        candidate = base
        suffix = 1
        while candidate in taken:
            suffix += 1
            tail = f"-{suffix}"
            candidate = f"{base[: HANDLE_MAX_LENGTH - len(tail)]}{tail}"
        taken.add(candidate)
        if candidate != profile.handle:
            profile.handle = candidate
            profile.save(update_fields=["handle"])


def noop(apps, schema_editor):
    """Lowercasing is not reversible; nothing to undo."""


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0005_linkclick"),
    ]

    operations = [
        # 1. Drop the case-sensitive unique constraint first so that
        #    lowercasing existing rows can't transiently violate it.
        migrations.AlterField(
            model_name="profile",
            name="handle",
            field=models.SlugField(
                help_text="Your public URL, e.g. /u/your-handle/",
                max_length=40,
                verbose_name="handle",
            ),
        ),
        # 2. Canonicalise existing data to lowercase.
        migrations.RunPython(normalize_handles, noop),
        # 3. Enforce case-insensitive uniqueness at the database level.
        migrations.AddConstraint(
            model_name="profile",
            constraint=models.UniqueConstraint(
                Lower("handle"),
                name="profiles_handle_ci_unique",
                violation_error_message="That handle is already taken.",
            ),
        ),
    ]

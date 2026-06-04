"""Delete analytics events (profile views + link clicks) past retention.

Run on a schedule (cron / Celery beat / systemd timer), e.g. daily:

    python manage.py prune_analytics

Use ``--days`` to override the window and ``--dry-run`` to preview.
"""

from __future__ import annotations

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.utils import timezone

from devresurge.profiles.models import ANALYTICS_RETENTION_DAYS
from devresurge.profiles.models import LinkClick
from devresurge.profiles.models import ProfileView

# Every prunable analytics model, in deletion order.
PRUNABLE_MODELS = (
    ("profile view", ProfileView),
    ("link click", LinkClick),
)


class Command(BaseCommand):
    help = "Delete analytics events (profile views + link clicks) older than the retention window."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--days",
            type=int,
            default=ANALYTICS_RETENTION_DAYS,
            help=f"Retention window in days (default: {ANALYTICS_RETENTION_DAYS}).",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Report what would be deleted without deleting anything.",
        )

    def handle(self, *args, **options) -> None:
        days = options["days"]
        dry_run = options["dry_run"]

        if days < 1:
            msg = "--days must be a positive integer."
            raise CommandError(msg)

        cutoff = timezone.now() - timedelta(days=days)
        total = 0

        for label, model in PRUNABLE_MODELS:
            if dry_run:
                count = model.objects.older_than(days).count()
                total += count
                self.stdout.write(
                    self.style.WARNING(
                        f"[dry-run] {count} {label} event(s) older than {days} days "
                        f"(before {cutoff:%Y-%m-%d %H:%M %Z}) would be deleted.",
                    ),
                )
                continue

            deleted = model.prune(days)
            total += deleted
            self.stdout.write(
                self.style.SUCCESS(
                    f"Deleted {deleted} {label} event(s) older than {days} days.",
                ),
            )

        verb = "would be deleted" if dry_run else "deleted"
        self.stdout.write(
            self.style.SUCCESS(f"Total: {total} analytics event(s) {verb}."),
        )

from django.core.management.base import BaseCommand

from devresurge.quizzes.catalog import seed_catalog


class Command(BaseCommand):
    help = "Seed starter quizzes and achievement badges."

    def add_arguments(self, parser):
        parser.add_argument(
            "--no-refresh-questions",
            action="store_true",
            help="Update quiz metadata only; leave existing questions alone.",
        )

    def handle(self, *args, **options):
        counts = seed_catalog(refresh_questions=not options["no_refresh_questions"])
        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded catalog — badges+{counts['badges']} quizzes+{counts['quizzes']} "
                f"questions+{counts['questions']}",
            ),
        )

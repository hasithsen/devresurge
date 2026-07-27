# Generated manually

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("connections", "0002_connection_relation_message_block"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notification",
            name="kind",
            field=models.CharField(
                choices=[
                    ("connection_request", "Connection request"),
                    ("connection_accepted", "Connection accepted"),
                    ("badge_earned", "Badge earned"),
                    ("quiz_passed", "Quiz passed"),
                    ("skill_endorsed", "Skill endorsed"),
                    ("recommendation", "Recommendation"),
                ],
                max_length=32,
                verbose_name="kind",
            ),
        ),
    ]

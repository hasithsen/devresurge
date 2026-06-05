from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="email_notifications",
            field=models.BooleanField(
                default=True,
                help_text="Receive emails about connection requests and activity.",
                verbose_name="email notifications",
            ),
        ),
    ]

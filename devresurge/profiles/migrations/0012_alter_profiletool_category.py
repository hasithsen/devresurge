# Devices / peripherals categories for ProfileTool

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0011_profiletool"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profiletool",
            name="category",
            field=models.CharField(
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
                    ("devices", "PCs & devices"),
                    ("peripherals", "Peripherals & desk"),
                    ("other", "Other"),
                ],
                default="other",
                max_length=24,
                verbose_name="category",
            ),
        ),
        migrations.AlterField(
            model_name="profiletool",
            name="note",
            field=models.CharField(
                blank=True,
                help_text="How you use it, or key specs — one short line.",
                max_length=160,
                verbose_name="note",
            ),
        ),
        migrations.AlterField(
            model_name="profiletool",
            name="url",
            field=models.URLField(
                blank=True,
                help_text="Optional docs, product, or store page.",
                max_length=300,
                verbose_name="URL",
            ),
        ),
    ]

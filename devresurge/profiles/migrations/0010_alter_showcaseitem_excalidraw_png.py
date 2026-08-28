# Excalidraw showcases use embedded .excalidraw.png (not live .excalidraw JSON)

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0009_practice_platforms"),
    ]

    operations = [
        migrations.AlterField(
            model_name="showcaseitem",
            name="github_url",
            field=models.URLField(
                help_text=(
                    "Public file link, e.g. "
                    "https://github.com/you/repo/blob/main/designs/api.excalidraw.png"
                ),
                max_length=500,
                verbose_name="GitHub file URL",
            ),
        ),
        migrations.AlterField(
            model_name="showcaseitem",
            name="kind",
            field=models.CharField(
                choices=[
                    ("excalidraw", "Excalidraw diagram (embedded PNG)"),
                    ("markdown", "Markdown notes"),
                    ("notes", "Plain / LFS-style notes"),
                    ("image", "Diagram / image"),
                ],
                default="markdown",
                max_length=20,
                verbose_name="kind",
            ),
        ),
    ]

# Align ProjectLink verbose names with the model Meta

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0012_alter_profiletool_category"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="projectlink",
            options={
                "ordering": ("order", "-created_at"),
                "verbose_name": "project",
                "verbose_name_plural": "projects",
            },
        ),
    ]

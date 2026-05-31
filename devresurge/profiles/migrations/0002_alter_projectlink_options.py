from django.db import migrations


class Migration(migrations.Migration):
    """Drop `-is_featured` from `ProjectLink` default ordering.

    Order is now fully user-driven via drag-and-drop on the projects list page,
    so the `featured` flag is a visual badge rather than a layout override.
    """

    dependencies = [
        ("profiles", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="projectlink",
            options={"ordering": ("order", "-created_at")},
        ),
    ]

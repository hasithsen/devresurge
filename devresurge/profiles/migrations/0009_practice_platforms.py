# Practice / contest platforms (LeetCode, HackerRank, …) on SocialLink

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0008_showcase_item"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sociallink",
            name="platform",
            field=models.CharField(
                choices=[
                    ("github", "GitHub"),
                    ("gitlab", "GitLab"),
                    ("leetcode", "LeetCode"),
                    ("hackerrank", "HackerRank"),
                    ("codeforces", "Codeforces"),
                    ("codewars", "Codewars"),
                    ("atcoder", "AtCoder"),
                    ("codesignal", "CodeSignal"),
                    ("topcoder", "TopCoder"),
                    ("exercism", "Exercism"),
                    ("kaggle", "Kaggle"),
                    ("codepen", "CodePen"),
                    ("huggingface", "Hugging Face"),
                    ("linkedin", "LinkedIn"),
                    ("twitter", "X / Twitter"),
                    ("mastodon", "Mastodon"),
                    ("bluesky", "Bluesky"),
                    ("stackoverflow", "Stack Overflow"),
                    ("devto", "Dev.to"),
                    ("medium", "Medium"),
                    ("youtube", "YouTube"),
                    ("website", "Personal Site"),
                    ("email", "Email"),
                    ("other", "Other"),
                ],
                default="website",
                max_length=32,
                verbose_name="platform",
            ),
        ),
    ]

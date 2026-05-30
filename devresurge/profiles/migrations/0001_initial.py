from django.conf import settings
from django.db import migrations
from django.db import models
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("handle", models.SlugField(help_text="Your public URL, e.g. /p/your-handle/", max_length=40, unique=True, verbose_name="handle")),
                ("display_name", models.CharField(blank=True, help_text="How your name appears on your profile.", max_length=120, verbose_name="display name")),
                ("headline", models.CharField(blank=True, help_text="A one-liner, e.g. 'Senior Backend Engineer · Python & Go'.", max_length=160, verbose_name="headline")),
                ("bio", models.TextField(blank=True, help_text="Markdown-style text describing who you are.", verbose_name="bio")),
                (
                    "primary_role",
                    models.CharField(
                        choices=[
                            ("backend", "Backend Engineer"),
                            ("frontend", "Frontend Engineer"),
                            ("fullstack", "Full Stack Engineer"),
                            ("mobile", "Mobile Engineer"),
                            ("devops", "DevOps / SRE"),
                            ("data", "Data Engineer / Analyst"),
                            ("ml", "ML / AI Engineer"),
                            ("security", "Security Engineer"),
                            ("qa", "QA / Test Engineer"),
                            ("design", "Product Designer"),
                            ("pm", "Product Manager"),
                            ("student", "Student / Learner"),
                            ("other", "Other"),
                        ],
                        default="other",
                        max_length=20,
                        verbose_name="primary role",
                    ),
                ),
                ("location", models.CharField(blank=True, max_length=120, verbose_name="location")),
                ("pronouns", models.CharField(blank=True, max_length=40, verbose_name="pronouns")),
                (
                    "years_experience",
                    models.PositiveSmallIntegerField(
                        default=0,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(60),
                        ],
                        verbose_name="years of experience",
                    ),
                ),
                ("tech_stack", models.CharField(blank=True, help_text="Comma-separated, e.g. 'python, django, postgres, aws'.", max_length=512, verbose_name="tech stack")),
                ("avatar", models.ImageField(blank=True, null=True, upload_to="avatars/", verbose_name="avatar")),
                ("website_url", models.URLField(blank=True, max_length=300, verbose_name="website")),
                ("show_email", models.BooleanField(default=False, verbose_name="show email publicly")),
                ("available_for_hire", models.BooleanField(default=False, verbose_name="available for hire")),
                ("is_public", models.BooleanField(default=True, verbose_name="publicly listed")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("-updated_at",),
            },
        ),
        migrations.AddIndex(
            model_name="profile",
            index=models.Index(fields=["primary_role"], name="profiles_primary_role_idx"),
        ),
        migrations.AddIndex(
            model_name="profile",
            index=models.Index(fields=["is_public"], name="profiles_is_public_idx"),
        ),
        migrations.CreateModel(
            name="ProjectLink",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=120, verbose_name="title")),
                ("description", models.CharField(blank=True, help_text="Short summary — 1-2 sentences.", max_length=280, verbose_name="description")),
                ("url", models.URLField(blank=True, max_length=300, verbose_name="live URL")),
                ("repo_url", models.URLField(blank=True, max_length=300, verbose_name="repository URL")),
                ("tech_stack", models.CharField(blank=True, help_text="Comma-separated.", max_length=240, verbose_name="tech stack")),
                ("is_featured", models.BooleanField(default=False, verbose_name="featured")),
                ("order", models.PositiveSmallIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="projects",
                        to="profiles.profile",
                    ),
                ),
            ],
            options={
                "ordering": ("-is_featured", "order", "-created_at"),
            },
        ),
        migrations.CreateModel(
            name="SocialLink",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "platform",
                    models.CharField(
                        choices=[
                            ("github", "GitHub"),
                            ("gitlab", "GitLab"),
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
                        max_length=24,
                        verbose_name="platform",
                    ),
                ),
                ("label", models.CharField(blank=True, help_text="Optional override for what the link reads as.", max_length=80, verbose_name="label")),
                ("url", models.CharField(max_length=300, verbose_name="URL")),
                ("order", models.PositiveSmallIntegerField(default=0)),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="social_links",
                        to="profiles.profile",
                    ),
                ),
            ],
            options={
                "ordering": ("order", "platform"),
            },
        ),
        migrations.AddConstraint(
            model_name="sociallink",
            constraint=models.UniqueConstraint(
                fields=("profile", "platform", "url"),
                name="profiles_sociallink_unique_url_per_platform",
            ),
        ),
    ]

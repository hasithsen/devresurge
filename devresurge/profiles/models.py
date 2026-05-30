from __future__ import annotations

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from slugify import slugify


HANDLE_MAX_LENGTH = 40
HANDLE_MIN_LENGTH = 2

MAX_AVATAR_BYTES = 2 * 1024 * 1024  # 2 MiB
ALLOWED_AVATAR_EXTENSIONS = ("jpg", "jpeg", "png", "webp", "gif")


def validate_avatar_size(value) -> None:
    """Reject avatar uploads larger than `MAX_AVATAR_BYTES`."""
    size = getattr(value, "size", None)
    if size is not None and size > MAX_AVATAR_BYTES:
        err = _("Avatar must be %(max)d MB or smaller.") % {
            "max": MAX_AVATAR_BYTES // (1024 * 1024),
        }
        raise ValidationError(err)


class PrimaryRole(models.TextChoices):
    BACKEND = "backend", _("Backend Engineer")
    FRONTEND = "frontend", _("Frontend Engineer")
    FULLSTACK = "fullstack", _("Full Stack Engineer")
    MOBILE = "mobile", _("Mobile Engineer")
    DEVOPS = "devops", _("DevOps / SRE")
    DATA = "data", _("Data Engineer / Analyst")
    ML = "ml", _("ML / AI Engineer")
    SECURITY = "security", _("Security Engineer")
    QA = "qa", _("QA / Test Engineer")
    DESIGN = "design", _("Product Designer")
    PM = "pm", _("Product Manager")
    STUDENT = "student", _("Student / Learner")
    OTHER = "other", _("Other")


class SocialPlatform(models.TextChoices):
    GITHUB = "github", "GitHub"
    GITLAB = "gitlab", "GitLab"
    LINKEDIN = "linkedin", "LinkedIn"
    TWITTER = "twitter", "X / Twitter"
    MASTODON = "mastodon", "Mastodon"
    BLUESKY = "bluesky", "Bluesky"
    STACKOVERFLOW = "stackoverflow", "Stack Overflow"
    DEVTO = "devto", "Dev.to"
    MEDIUM = "medium", "Medium"
    YOUTUBE = "youtube", "YouTube"
    WEBSITE = "website", "Personal Site"
    EMAIL = "email", "Email"
    OTHER = "other", "Other"


class Profile(models.Model):
    """An IT professional's public profile."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    handle = models.SlugField(
        _("handle"),
        max_length=HANDLE_MAX_LENGTH,
        unique=True,
        help_text=_("Your public URL, e.g. /p/your-handle/"),
    )
    display_name = models.CharField(
        _("display name"),
        max_length=120,
        blank=True,
        help_text=_("How your name appears on your profile."),
    )
    headline = models.CharField(
        _("headline"),
        max_length=160,
        blank=True,
        help_text=_("A one-liner, e.g. 'Senior Backend Engineer · Python & Go'."),
    )
    bio = models.TextField(
        _("bio"),
        blank=True,
        help_text=_("Markdown-style text describing who you are."),
    )
    primary_role = models.CharField(
        _("primary role"),
        max_length=20,
        choices=PrimaryRole.choices,
        default=PrimaryRole.OTHER,
    )
    location = models.CharField(_("location"), max_length=120, blank=True)
    years_experience = models.PositiveSmallIntegerField(
        _("years of experience"),
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(60)],
    )
    tech_stack = models.CharField(
        _("tech stack"),
        max_length=512,
        blank=True,
        help_text=_("Comma-separated, e.g. 'python, django, postgres, aws'."),
    )
    avatar = models.ImageField(
        _("avatar"),
        upload_to="avatars/",
        blank=True,
        null=True,
        help_text=_(
            "Square image works best. Max 2 MB. JPG, PNG, WEBP or GIF.",
        ),
        validators=[
            validate_avatar_size,
            FileExtensionValidator(allowed_extensions=list(ALLOWED_AVATAR_EXTENSIONS)),
        ],
    )
    website_url = models.URLField(_("website"), max_length=300, blank=True)
    show_email = models.BooleanField(_("show email publicly"), default=False)
    available_for_hire = models.BooleanField(_("available for hire"), default=False)
    is_public = models.BooleanField(_("publicly listed"), default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated_at",)
        indexes = [
            models.Index(fields=["primary_role"], name="profiles_primary_role_idx"),
            models.Index(fields=["is_public"], name="profiles_is_public_idx"),
        ]

    def __str__(self) -> str:
        return self.display_name or self.handle

    def get_absolute_url(self) -> str:
        return reverse("profiles:public", kwargs={"handle": self.handle})

    @property
    def tech_stack_list(self) -> list[str]:
        seen: set[str] = set()
        out: list[str] = []
        for raw in self.tech_stack.split(","):
            tag = raw.strip().lower()
            if tag and tag not in seen:
                seen.add(tag)
                out.append(tag)
        return out

    @property
    def initials(self) -> str:
        name = (self.display_name or self.handle or "?").strip()
        parts = [p for p in name.split() if p]
        if not parts:
            return "?"
        if len(parts) == 1:
            return parts[0][:2].upper()
        return (parts[0][0] + parts[-1][0]).upper()

    def ensure_handle(self) -> None:
        """Populate `handle` from a sensible source if it is empty."""
        if self.handle:
            return
        seed = self.display_name or (self.user.name if self.user_id else "") or ""
        if not seed and self.user_id and self.user.email:
            seed = self.user.email.split("@")[0]
        candidate = slugify(seed) or "dev"
        candidate = candidate[:HANDLE_MAX_LENGTH] or "dev"

        base = candidate
        suffix = 1
        existing = Profile.objects.exclude(pk=self.pk)
        while existing.filter(handle=candidate).exists():
            suffix += 1
            tail = f"-{suffix}"
            candidate = f"{base[: HANDLE_MAX_LENGTH - len(tail)]}{tail}"
        self.handle = candidate

    def save(self, *args, **kwargs) -> None:
        self.ensure_handle()
        super().save(*args, **kwargs)


class ProjectLink(models.Model):
    """A project a user wants to highlight on their profile."""

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="projects",
    )
    title = models.CharField(_("title"), max_length=120)
    description = models.CharField(
        _("description"),
        max_length=280,
        blank=True,
        help_text=_("Short summary — 1-2 sentences."),
    )
    url = models.URLField(_("live URL"), max_length=300, blank=True)
    repo_url = models.URLField(_("repository URL"), max_length=300, blank=True)
    tech_stack = models.CharField(
        _("tech stack"),
        max_length=240,
        blank=True,
        help_text=_("Comma-separated."),
    )
    is_featured = models.BooleanField(_("featured"), default=False)
    order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-is_featured", "order", "-created_at")

    def __str__(self) -> str:
        return self.title

    @property
    def tech_stack_list(self) -> list[str]:
        seen: set[str] = set()
        out: list[str] = []
        for raw in self.tech_stack.split(","):
            tag = raw.strip().lower()
            if tag and tag not in seen:
                seen.add(tag)
                out.append(tag)
        return out


class SocialLink(models.Model):
    """A link to a user's presence on an external platform."""

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="social_links",
    )
    platform = models.CharField(
        _("platform"),
        max_length=24,
        choices=SocialPlatform.choices,
        default=SocialPlatform.WEBSITE,
    )
    label = models.CharField(
        _("label"),
        max_length=80,
        blank=True,
        help_text=_("Optional override for what the link reads as."),
    )
    url = models.CharField(_("URL"), max_length=300)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("order", "platform")
        constraints = [
            models.UniqueConstraint(
                fields=("profile", "platform", "url"),
                name="profiles_sociallink_unique_url_per_platform",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.get_platform_display()}: {self.label or self.url}"

    @property
    def display_label(self) -> str:
        return self.label or self.get_platform_display()

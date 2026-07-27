from __future__ import annotations

from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.functions import Lower
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from slugify import slugify


HANDLE_MAX_LENGTH = 40
HANDLE_MIN_LENGTH = 2

MAX_AVATAR_BYTES = 2 * 1024 * 1024  # 2 MiB
ALLOWED_AVATAR_EXTENSIONS = ("jpg", "jpeg", "png", "webp", "gif")

# How long raw analytics events are kept before pruning.
ANALYTICS_RETENTION_DAYS = 90


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
    """A tech professional's public profile."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    handle = models.SlugField(
        _("handle"),
        max_length=HANDLE_MAX_LENGTH,
        # Uniqueness is enforced case-insensitively at the DB via a
        # `Lower("handle")` UniqueConstraint (see Meta.constraints). The
        # SlugField's default db_index keeps exact (lowercased) lookups fast.
        help_text=_("Your public URL, e.g. /u/your-handle/"),
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
    available_for_hire = models.BooleanField(_("open to work"), default=False)
    open_to_collaborate = models.BooleanField(
        _("open to collaborate"),
        default=False,
        help_text=_("Side projects, OSS, or consulting together."),
    )
    open_to_mentor = models.BooleanField(
        _("open to mentor"),
        default=False,
        help_text=_("Happy to mentor others."),
    )
    open_to_learning = models.BooleanField(
        _("seeking mentorship"),
        default=False,
        help_text=_("Looking for guidance from more senior folks."),
    )
    open_to_note = models.CharField(
        _("open-to note"),
        max_length=200,
        blank=True,
        help_text=_("Optional one-liner for recruiters / collaborators."),
    )
    is_public = models.BooleanField(_("publicly listed"), default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated_at",)
        constraints = [
            models.UniqueConstraint(
                Lower("handle"),
                name="profiles_handle_ci_unique",
                violation_error_message=_("That handle is already taken."),
            ),
        ]
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
    def public_name(self) -> str:
        """Public-facing label for this user.

        Prefers the chosen display name, falling back to the public `@handle`.
        Deliberately never exposes the account email address.
        """
        return self.display_name or f"@{self.handle}"

    @property
    def initials(self) -> str:
        name = (self.display_name or self.handle or "?").strip()
        parts = [p for p in name.split() if p]
        if not parts:
            return "?"
        if len(parts) == 1:
            return parts[0][:2].upper()
        return (parts[0][0] + parts[-1][0]).upper()

    @staticmethod
    def normalize_handle(value: str | None) -> str:
        """Canonical form of a handle — lowercased and trimmed.

        Handles are case-insensitive: we store and compare the lowercase form
        so `/u/Ada/` and `/u/ada/` always resolve to the same profile.
        """
        return (value or "").strip().lower()

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
        while existing.filter(handle__iexact=candidate).exists():
            suffix += 1
            tail = f"-{suffix}"
            candidate = f"{base[: HANDLE_MAX_LENGTH - len(tail)]}{tail}"
        self.handle = candidate

    def save(self, *args, **kwargs) -> None:
        self.ensure_handle()
        # Canonicalise to lowercase regardless of entry path (form, admin, ORM).
        self.handle = self.normalize_handle(self.handle)
        super().save(*args, **kwargs)

    def readiness_checks(self) -> list[dict]:
        """Checklist of profile fields that make a share-ready public page.

        Each item is ``{key, label, done, url_name}`` so the dashboard can
        render a progress bar and deep-link to the right editor.
        """
        has_projects = self.projects.exists() if self.pk else False
        has_links = bool(self.website_url) or (
            self.social_links.exists() if self.pk else False
        )
        has_experience = self.experiences.exists() if self.pk else False
        has_linkedin = False
        if self.pk:
            has_linkedin = self.social_links.filter(platform=SocialPlatform.LINKEDIN).exists()
        return [
            {
                "key": "display_name",
                "label": _("Display name"),
                "done": bool(self.display_name),
                "url_name": "profiles:edit",
            },
            {
                "key": "headline",
                "label": _("Headline"),
                "done": bool(self.headline),
                "url_name": "profiles:edit",
            },
            {
                "key": "bio",
                "label": _("Bio"),
                "done": bool(self.bio.strip() if self.bio else ""),
                "url_name": "profiles:edit",
            },
            {
                "key": "avatar",
                "label": _("Avatar"),
                "done": bool(self.avatar),
                "url_name": "profiles:edit",
            },
            {
                "key": "tech_stack",
                "label": _("Tech stack"),
                "done": bool(self.tech_stack_list),
                "url_name": "profiles:edit",
            },
            {
                "key": "experience",
                "label": _("Work experience"),
                "done": has_experience,
                "url_name": "profiles:experience_create",
            },
            {
                "key": "projects",
                "label": _("At least one project"),
                "done": has_projects,
                "url_name": "profiles:project_create",
            },
            {
                "key": "links",
                "label": _("Social or website link"),
                "done": has_links,
                "url_name": "profiles:link_create",
            },
            {
                "key": "linkedin",
                "label": _("LinkedIn link (bridge)"),
                "done": has_linkedin,
                "url_name": "profiles:link_create",
            },
            {
                "key": "public",
                "label": _("Publicly listed"),
                "done": bool(self.is_public),
                "url_name": "profiles:edit",
            },
        ]

    def readiness(self) -> dict:
        """Aggregate readiness score for the owner dashboard."""
        checks = self.readiness_checks()
        done = sum(1 for c in checks if c["done"])
        total = len(checks)
        pct = round((done / total) * 100) if total else 100
        return {
            "checks": checks,
            "done": done,
            "total": total,
            "pct": pct,
            "complete": done == total,
        }

    def to_readme_markdown(self, *, base_url: str = "") -> str:
        """Serialize this profile as a shareable README.md document."""
        name = self.display_name or self.handle
        lines: list[str] = [f"# {name}", ""]
        if self.headline:
            lines.extend([f"*{self.headline}*", ""])

        meta: list[str] = [f"**@{self.handle}**", self.get_primary_role_display()]
        if self.location:
            meta.append(self.location)
        if self.years_experience:
            meta.append(f"{self.years_experience} yr experience")
        if self.available_for_hire:
            meta.append("open to work")
        if self.open_to_collaborate:
            meta.append("open to collaborate")
        if self.open_to_mentor:
            meta.append("open to mentor")
        if self.open_to_learning:
            meta.append("seeking mentorship")
        lines.append(" · ".join(meta))
        lines.append("")
        if self.open_to_note:
            lines.extend([f"> {self.open_to_note}", ""])

        if self.tech_stack_list:
            lines.extend(["## Stack", "", ", ".join(f"`{t}`" for t in self.tech_stack_list), ""])

        if self.bio:
            lines.extend(["## About", "", self.bio.strip(), ""])

        experiences = list(self.experiences.all()) if self.pk else []
        if experiences:
            lines.extend(["## Experience", ""])
            for exp in experiences:
                when = exp.date_range_label
                lines.append(f"### {exp.title} · {exp.company}")
                lines.append("")
                lines.append(f"*{when}*")
                if exp.description:
                    lines.append("")
                    lines.append(exp.description.strip())
                lines.append("")

        education = list(self.education.all()) if self.pk else []
        if education:
            lines.extend(["## Education", ""])
            for edu in education:
                lines.append(f"- **{edu.school}** — {edu.degree_label}" + (f" ({edu.year_label})" if edu.year_label else ""))
            lines.append("")

        projects = list(self.projects.all()) if self.pk else []
        if projects:
            lines.extend(["## Projects", ""])
            for project in projects:
                title = f"★ {project.title}" if project.is_featured else project.title
                link = project.url or project.repo_url
                heading = f"### [{title}]({link})" if link else f"### {title}"
                lines.append(heading)
                if project.description:
                    lines.append("")
                    lines.append(project.description)
                if project.tech_stack_list:
                    lines.append("")
                    lines.append(", ".join(f"`{t}`" for t in project.tech_stack_list))
                extras: list[str] = []
                if project.url and project.repo_url:
                    extras.append(f"[live]({project.url})")
                    extras.append(f"[repo]({project.repo_url})")
                if extras:
                    lines.append("")
                    lines.append(" · ".join(extras))
                lines.append("")

        recommendations = list(self.recommendations_received.filter(is_public=True)[:5]) if self.pk else []
        if recommendations:
            lines.extend(["## Recommendations", ""])
            for rec in recommendations:
                author = rec.author.profile.public_name if hasattr(rec.author, "profile") else "a peer"
                lines.append(f"> {rec.body.strip()}")
                lines.append(f"> — {author}")
                lines.append("")

        links: list[str] = []
        if self.website_url:
            links.append(f"- [Website]({self.website_url})")
        if self.show_email and self.user_id and self.user.email:
            links.append(f"- [Email](mailto:{self.user.email})")
        if self.pk:
            for link in self.social_links.all():
                links.append(f"- [{link.display_label}]({link.url})")
        if links:
            lines.extend(["## Links", "", *links, ""])

        if base_url:
            lines.extend(
                [
                    "---",
                    "",
                    f"Profile: {base_url}{self.get_absolute_url()}",
                    "",
                    "_Technical signal on DevResurge — career network on LinkedIn._",
                    "",
                ],
            )
        return "\n".join(lines)

    @property
    def open_to_labels(self) -> list[str]:
        """Human labels for active open-to intents."""
        labels: list[str] = []
        if self.available_for_hire:
            labels.append(str(_("open to work")))
        if self.open_to_collaborate:
            labels.append(str(_("collaborate")))
        if self.open_to_mentor:
            labels.append(str(_("mentor")))
        if self.open_to_learning:
            labels.append(str(_("seeking mentor")))
        return labels

    def linkedin_url(self) -> str:
        if not self.pk:
            return ""
        link = self.social_links.filter(platform=SocialPlatform.LINKEDIN).first()
        return link.url if link else ""



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
        # `order` is the user-controlled rank (drag-and-drop on the list page).
        # `is_featured` is a visual badge, not a layout override.
        ordering = ("order", "-created_at")

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


class WorkExperience(models.Model):
    """A role on the career timeline — LinkedIn-complementary, signal-first."""

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="experiences",
    )
    title = models.CharField(_("title"), max_length=120)
    company = models.CharField(_("company"), max_length=120)
    location = models.CharField(_("location"), max_length=120, blank=True)
    description = models.TextField(
        _("description"),
        blank=True,
        help_text=_("What you shipped — Markdown-lite plain text is fine."),
    )
    start_year = models.PositiveSmallIntegerField(
        _("start year"),
        validators=[MinValueValidator(1970), MaxValueValidator(2100)],
    )
    start_month = models.PositiveSmallIntegerField(
        _("start month"),
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(12)],
    )
    end_year = models.PositiveSmallIntegerField(
        _("end year"),
        null=True,
        blank=True,
        validators=[MinValueValidator(1970), MaxValueValidator(2100)],
    )
    end_month = models.PositiveSmallIntegerField(
        _("end month"),
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(12)],
    )
    is_current = models.BooleanField(_("current role"), default=False)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("order", "-start_year", "-start_month")
        verbose_name = _("work experience")
        verbose_name_plural = _("work experience")

    def __str__(self) -> str:
        return f"{self.title} @ {self.company}"

    def clean(self) -> None:
        super().clean()
        if self.is_current:
            self.end_year = None
            self.end_month = None
        elif self.end_year and self.start_year:
            if (self.end_year, self.end_month or 12) < (self.start_year, self.start_month):
                raise ValidationError(_("End date must be after start date."))

    @property
    def date_range_label(self) -> str:
        start = f"{self.start_year}-{self.start_month:02d}"
        if self.is_current or not self.end_year:
            return f"{start} — present"
        end = f"{self.end_year}-{self.end_month or 12:02d}"
        return f"{start} — {end}"


class Education(models.Model):
    """School / bootcamp entry for the public timeline."""

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="education",
    )
    school = models.CharField(_("school"), max_length=160)
    degree = models.CharField(
        _("degree"),
        max_length=120,
        blank=True,
        help_text=_("e.g. BSc Computer Science, Bootcamp"),
    )
    field = models.CharField(_("field of study"), max_length=120, blank=True)
    start_year = models.PositiveSmallIntegerField(
        _("start year"),
        null=True,
        blank=True,
        validators=[MinValueValidator(1970), MaxValueValidator(2100)],
    )
    end_year = models.PositiveSmallIntegerField(
        _("end year"),
        null=True,
        blank=True,
        validators=[MinValueValidator(1970), MaxValueValidator(2100)],
    )
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("order", "-end_year", "-start_year")
        verbose_name = _("education")
        verbose_name_plural = _("education")

    def __str__(self) -> str:
        return self.school

    @property
    def degree_label(self) -> str:
        parts = [p for p in (self.degree, self.field) if p]
        return " · ".join(parts) if parts else ""

    @property
    def year_label(self) -> str:
        if self.start_year and self.end_year:
            return f"{self.start_year}–{self.end_year}"
        if self.end_year:
            return str(self.end_year)
        if self.start_year:
            return f"{self.start_year}–"
        return ""


class SkillEndorsement(models.Model):
    """A connection vouching for one skill on another member's stack.

    Only accepted connections may endorse, and only skills listed on the
    profile's tech_stack. This is peer signal — complementary to LinkedIn's
    looser endorsement model.
    """

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="endorsements",
    )
    endorser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="endorsements_given",
    )
    skill = models.CharField(_("skill"), max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("skill endorsement")
        verbose_name_plural = _("skill endorsements")
        constraints = [
            models.UniqueConstraint(
                fields=("profile", "endorser", "skill"),
                name="profiles_endorsement_unique",
            ),
        ]
        indexes = [
            models.Index(fields=["profile", "skill"], name="profiles_endorse_skill_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.endorser_id} → {self.profile_id}:{self.skill}"

    def clean(self) -> None:
        super().clean()
        skill = (self.skill or "").strip().lower()
        self.skill = skill
        if self.profile_id and skill not in self.profile.tech_stack_list:
            raise ValidationError(_("Skill must be on the member's tech stack."))
        if self.profile_id and self.endorser_id == self.profile.user_id:
            raise ValidationError(_("You can't endorse yourself."))


class Recommendation(models.Model):
    """A short written recommendation from an accepted connection."""

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="recommendations_received",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recommendations_written",
    )
    relationship = models.CharField(
        _("relationship"),
        max_length=80,
        blank=True,
        help_text=_("e.g. Worked together at Acme, mentored on Django"),
    )
    body = models.TextField(_("recommendation"), max_length=800)
    is_public = models.BooleanField(_("visible on profile"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("recommendation")
        verbose_name_plural = _("recommendations")
        constraints = [
            models.UniqueConstraint(
                fields=("profile", "author"),
                name="profiles_recommendation_unique_author",
            ),
        ]

    def __str__(self) -> str:
        return f"rec by {self.author_id} → {self.profile_id}"

    def clean(self) -> None:
        super().clean()
        if self.profile_id and self.author_id == self.profile.user_id:
            raise ValidationError(_("You can't recommend yourself."))


class AnalyticsEventQuerySet(models.QuerySet):
    """Shared query helpers for the time-bucketed analytics event logs."""

    def for_profile(self, profile) -> AnalyticsEventQuerySet:
        return self.filter(profile=profile)

    def within_days(self, days: int) -> AnalyticsEventQuerySet:
        """Events from the last `days` calendar days (inclusive of today)."""
        start = timezone.localdate() - timedelta(days=days - 1)
        return self.filter(created_at__date__gte=start)

    def older_than(self, days: int) -> AnalyticsEventQuerySet:
        cutoff = timezone.now() - timedelta(days=days)
        return self.filter(created_at__lt=cutoff)


class PrunableEventMixin:
    """Mixin giving analytics models a shared retention window + `prune`.

    Concrete models must expose an `objects` manager built from
    `AnalyticsEventQuerySet` (so `older_than` is available).
    """

    RETENTION_DAYS = ANALYTICS_RETENTION_DAYS

    @classmethod
    def prune(cls, days: int | None = None) -> int:
        """Delete events older than the retention window. Returns rows removed."""
        days = cls.RETENTION_DAYS if days is None else days
        deleted, _ = cls.objects.older_than(days).delete()
        return deleted


class ProfileView(PrunableEventMixin, models.Model):
    """A single visit to a public profile page.

    Stored as privacy-preserving event rows — we keep a salted, irreversible
    `visitor_hash` (never a raw IP) so we can count unique visitors without
    retaining personal data. Rows older than `RETENTION_DAYS` are pruned by the
    `prune_analytics` management command (see `prune`).
    """

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="views",
    )
    visitor_hash = models.CharField(
        _("visitor hash"),
        max_length=64,
        db_index=True,
        help_text=_("Salted SHA-256 of IP + user agent. Not reversible."),
    )
    referrer = models.CharField(
        _("referrer host"),
        max_length=255,
        blank=True,
        help_text=_("Host the visitor arrived from, e.g. 'news.ycombinator.com'."),
    )
    is_unique = models.BooleanField(
        _("first view of day"),
        default=False,
        help_text=_("True if this visitor's first view of this profile that day."),
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    objects = AnalyticsEventQuerySet.as_manager()

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("profile view")
        verbose_name_plural = _("profile views")
        indexes = [
            models.Index(
                fields=["profile", "created_at"],
                name="profiles_pv_prof_created_idx",
            ),
            models.Index(
                fields=["profile", "visitor_hash"],
                name="profiles_pv_prof_visitor_idx",
            ),
        ]

    def __str__(self) -> str:
        return f"view of {self.profile_id} @ {self.created_at:%Y-%m-%d %H:%M}"


class LinkKind(models.TextChoices):
    PROJECT = "project", _("Project")
    SOCIAL = "social", _("Social")
    WEBSITE = "website", _("Website")
    EMAIL = "email", _("Email")


class LinkClick(PrunableEventMixin, models.Model):
    """An outbound click on a link shown on a public profile.

    Recorded via a CSRF-exempt beacon endpoint (see `views.link_click_view`).
    `label` / `destination` are snapshots so stats survive the underlying
    project/social link being edited or deleted. Shares the 90-day retention
    window and `prune` with `ProfileView`.
    """

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="link_clicks",
    )
    kind = models.CharField(
        _("link kind"),
        max_length=20,
        choices=LinkKind.choices,
    )
    target_id = models.PositiveBigIntegerField(
        _("target id"),
        null=True,
        blank=True,
        help_text=_("PK of the clicked ProjectLink/SocialLink, if applicable."),
    )
    label = models.CharField(_("label"), max_length=160, blank=True)
    destination = models.CharField(
        _("destination host"),
        max_length=255,
        blank=True,
        help_text=_("Host the click leads to, e.g. 'github.com'."),
    )
    visitor_hash = models.CharField(
        _("visitor hash"),
        max_length=64,
        db_index=True,
        help_text=_("Salted SHA-256 of IP + user agent. Not reversible."),
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    objects = AnalyticsEventQuerySet.as_manager()

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("link click")
        verbose_name_plural = _("link clicks")
        indexes = [
            models.Index(
                fields=["profile", "created_at"],
                name="profiles_lc_prof_created_idx",
            ),
            models.Index(
                fields=["profile", "kind"],
                name="profiles_lc_prof_kind_idx",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.kind} click on {self.profile_id} @ {self.created_at:%Y-%m-%d}"

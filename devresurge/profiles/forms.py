from __future__ import annotations

from pathlib import Path

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from slugify import slugify

from .models import ALLOWED_AVATAR_EXTENSIONS
from .models import HANDLE_MAX_LENGTH
from .models import HANDLE_MIN_LENGTH
from .models import MAX_AVATAR_BYTES
from .models import PLATFORM_PROFILE_URLS
from .models import PLATFORM_URL_HINTS
from .models import Education
from .models import Profile
from .models import ProjectLink
from .models import Recommendation
from .models import ShowcaseItem
from .models import SocialLink
from .models import SocialPlatform
from .models import WorkExperience

_ALLOWED_AVATAR_MIME = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/gif",
}

# Optgroups so DevResurge feels like the hub for practice + professional signal.
PLATFORM_CHOICE_GROUPS: list[tuple[str, list[tuple[str, str]]]] = [
    (
        _("Code & practice"),
        [
            (SocialPlatform.LEETCODE, SocialPlatform.LEETCODE.label),
            (SocialPlatform.HACKERRANK, SocialPlatform.HACKERRANK.label),
            (SocialPlatform.CODEFORCES, SocialPlatform.CODEFORCES.label),
            (SocialPlatform.CODEWARS, SocialPlatform.CODEWARS.label),
            (SocialPlatform.ATCODER, SocialPlatform.ATCODER.label),
            (SocialPlatform.CODESIGNAL, SocialPlatform.CODESIGNAL.label),
            (SocialPlatform.TOPCODER, SocialPlatform.TOPCODER.label),
            (SocialPlatform.EXERCISM, SocialPlatform.EXERCISM.label),
            (SocialPlatform.KAGGLE, SocialPlatform.KAGGLE.label),
            (SocialPlatform.CODEPEN, SocialPlatform.CODEPEN.label),
            (SocialPlatform.HUGGINGFACE, SocialPlatform.HUGGINGFACE.label),
        ],
    ),
    (
        _("Code hosting"),
        [
            (SocialPlatform.GITHUB, SocialPlatform.GITHUB.label),
            (SocialPlatform.GITLAB, SocialPlatform.GITLAB.label),
        ],
    ),
    (
        _("Professional"),
        [
            (SocialPlatform.LINKEDIN, SocialPlatform.LINKEDIN.label),
            (SocialPlatform.STACKOVERFLOW, SocialPlatform.STACKOVERFLOW.label),
            (SocialPlatform.WEBSITE, SocialPlatform.WEBSITE.label),
            (SocialPlatform.EMAIL, SocialPlatform.EMAIL.label),
        ],
    ),
    (
        _("Writing & media"),
        [
            (SocialPlatform.DEVTO, SocialPlatform.DEVTO.label),
            (SocialPlatform.MEDIUM, SocialPlatform.MEDIUM.label),
            (SocialPlatform.YOUTUBE, SocialPlatform.YOUTUBE.label),
            (SocialPlatform.TWITTER, SocialPlatform.TWITTER.label),
            (SocialPlatform.MASTODON, SocialPlatform.MASTODON.label),
            (SocialPlatform.BLUESKY, SocialPlatform.BLUESKY.label),
        ],
    ),
    (
        _("Other"),
        [
            (SocialPlatform.OTHER, SocialPlatform.OTHER.label),
        ],
    ),
]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "handle",
            "display_name",
            "headline",
            "primary_role",
            "bio",
            "location",
            "years_experience",
            "tech_stack",
            "avatar",
            "website_url",
            "show_email",
            "available_for_hire",
            "open_to_collaborate",
            "open_to_mentor",
            "open_to_learning",
            "open_to_note",
            "is_public",
        )
        widgets = {
            "bio": forms.Textarea(
                attrs={
                    "rows": 6,
                    "placeholder": "# about\n\nI ship **reliable** systems.\n\n- python\n- django",
                },
            ),
            "headline": forms.TextInput(attrs={"placeholder": "Senior Backend Engineer ? Python & Go"}),
            "tech_stack": forms.TextInput(attrs={"placeholder": "python, django, postgres, aws"}),
            "handle": forms.TextInput(attrs={"placeholder": "your-handle"}),
            "avatar": forms.ClearableFileInput(
                attrs={
                    "accept": "image/jpeg,image/png,image/webp,image/gif",
                    "data-avatar-input": "",
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["bio"].help_text = _(
            "Markdown supported: headings, lists, bold, italic, code, and links.",
        )

    def clean_avatar(self):
        """Defence-in-depth ? model validators run too, but better UX here."""
        avatar = self.cleaned_data.get("avatar")
        if not avatar:
            return avatar
        # If the value is a previously-uploaded file (not a fresh upload), skip.
        if not hasattr(avatar, "content_type"):
            return avatar
        size = getattr(avatar, "size", 0)
        if size and size > MAX_AVATAR_BYTES:
            err = _("Avatar must be %(max)d MB or smaller (got %(got).1f MB).") % {
                "max": MAX_AVATAR_BYTES // (1024 * 1024),
                "got": size / (1024 * 1024),
            }
            raise ValidationError(err)
        content_type = (avatar.content_type or "").lower()
        if content_type and content_type not in _ALLOWED_AVATAR_MIME:
            err = _("Unsupported image type. Use JPG, PNG, WEBP or GIF.")
            raise ValidationError(err)
        ext = Path(getattr(avatar, "name", "")).suffix.lower().lstrip(".")
        if ext and ext not in ALLOWED_AVATAR_EXTENSIONS:
            err = _("Unsupported file extension. Use JPG, PNG, WEBP or GIF.")
            raise ValidationError(err)
        return avatar

    def clean_handle(self) -> str:
        raw = (self.cleaned_data.get("handle") or "").strip().lower()
        if not raw:
            err = _("Handle is required.")
            raise ValidationError(err)
        normalized = slugify(raw)
        if normalized != raw:
            err = _("Handles may only contain lowercase letters, numbers and hyphens.")
            raise ValidationError(err)
        if not (HANDLE_MIN_LENGTH <= len(normalized) <= HANDLE_MAX_LENGTH):
            err = _("Handles must be between %(lo)d and %(hi)d characters.") % {
                "lo": HANDLE_MIN_LENGTH,
                "hi": HANDLE_MAX_LENGTH,
            }
            raise ValidationError(err)
        if Profile.objects.exclude(pk=self.instance.pk).filter(handle__iexact=normalized).exists():
            err = _("That handle is already taken.")
            raise ValidationError(err)
        return normalized


class ProjectLinkForm(forms.ModelForm):
    class Meta:
        model = ProjectLink
        # `order` is managed via drag-and-drop on the list page, not the form.
        fields = (
            "title",
            "description",
            "url",
            "repo_url",
            "tech_stack",
            "is_featured",
        )
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3, "placeholder": "What it does, in one breath."}),
            "tech_stack": forms.TextInput(attrs={"placeholder": "python, fastapi, postgres"}),
        }

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get("url") and not cleaned.get("repo_url"):
            err = _("Provide at least a live URL or a repository URL.")
            raise ValidationError(err)
        return cleaned


class SocialLinkForm(forms.ModelForm):
    class Meta:
        model = SocialLink
        # `order` is managed via drag-and-drop on the list page, not the form.
        fields = ("platform", "label", "url")
        widgets = {
            "url": forms.TextInput(
                attrs={
                    "placeholder": "https://leetcode.com/u/your-handle/  or  your-handle",
                    "autocomplete": "url",
                },
            ),
            "label": forms.TextInput(attrs={"placeholder": "Optional display name"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["platform"].choices = PLATFORM_CHOICE_GROUPS
        self.fields["platform"].help_text = _(
            "Bring LeetCode, HackerRank, and the rest here ? DevResurge is the hub.",
        )
        self.fields["url"].help_text = _(
            "Full profile URL, or just your handle for known sites (we expand it).",
        )
        platform = None
        if self.is_bound:
            platform = self.data.get("platform")
        elif self.instance and self.instance.pk:
            platform = self.instance.platform
        elif self.initial.get("platform"):
            platform = self.initial["platform"]
        hint = PLATFORM_URL_HINTS.get(platform or "")
        if hint:
            self.fields["url"].widget.attrs["placeholder"] = hint

    def clean_url(self) -> str:
        url = (self.cleaned_data.get("url") or "").strip()
        platform = self.cleaned_data.get("platform")
        if not url:
            err = _("Enter a URL or profile handle.")
            raise ValidationError(err)
        if platform == SocialPlatform.EMAIL:
            if "@" not in url:
                err = _("Enter a valid email address.")
                raise ValidationError(err)
            if not url.lower().startswith("mailto:"):
                url = f"mailto:{url}"
            return url
        # Bare handle ? canonical public profile URL for known platforms.
        if "://" not in url and platform in PLATFORM_PROFILE_URLS:
            handle = url.lstrip("@").strip().strip("/")
            if not handle or any(ch.isspace() for ch in handle):
                err = _("Enter a valid profile handle or full URL.")
                raise ValidationError(err)
            url = PLATFORM_PROFILE_URLS[platform].format(handle=handle)
        validator = forms.URLField()
        try:
            url = validator.clean(url)
        except ValidationError as exc:
            raise ValidationError(_("Enter a valid URL (or a handle for this platform).")) from exc
        return url


class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        fields = (
            "title",
            "company",
            "location",
            "description",
            "start_year",
            "start_month",
            "end_year",
            "end_month",
            "is_current",
        )
        widgets = {
            "description": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Shipped X, led Y, reduced Z?"},
            ),
            "title": forms.TextInput(attrs={"placeholder": "Senior Backend Engineer"}),
            "company": forms.TextInput(attrs={"placeholder": "Acme"}),
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("is_current"):
            cleaned["end_year"] = None
            cleaned["end_month"] = None
        return cleaned


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ("school", "degree", "field", "start_year", "end_year")
        widgets = {
            "school": forms.TextInput(attrs={"placeholder": "University / Bootcamp"}),
            "degree": forms.TextInput(attrs={"placeholder": "BSc / Certificate"}),
            "field": forms.TextInput(attrs={"placeholder": "Computer Science"}),
        }


class RecommendationForm(forms.ModelForm):
    class Meta:
        model = Recommendation
        fields = ("relationship", "body")
        widgets = {
            "relationship": forms.TextInput(
                attrs={"placeholder": "Worked together on API platform"},
            ),
            "body": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "What they?re strong at, and how you know.",
                    "maxlength": 800,
                },
            ),
        }

    def clean_body(self) -> str:
        body = (self.cleaned_data.get("body") or "").strip()
        if len(body) < 40:
            raise ValidationError(_("Write at least a couple of sentences (40+ chars)."))
        return body


class ShowcaseItemForm(forms.ModelForm):
    sync_now = forms.BooleanField(
        required=False,
        initial=True,
        label=_("Fetch from GitHub now"),
        help_text=_("Pull the public file into DevResurge so visitors can read it here."),
    )

    class Meta:
        model = ShowcaseItem
        fields = (
            "title",
            "summary",
            "kind",
            "github_url",
            "tags",
            "is_featured",
            "is_published",
        )
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "URL shortener ? system design"},
            ),
            "summary": forms.Textarea(
                attrs={
                    "rows": 2,
                    "placeholder": "Excalidraw walkthrough of a FAANG-style design round.",
                },
            ),
            "github_url": forms.URLInput(
                attrs={
                    "placeholder": "https://github.com/you/lab/blob/main/designs/url-shortener.excalidraw.png",
                },
            ),
            "tags": forms.TextInput(
                attrs={"placeholder": "system-design, excalidraw, linux"},
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["kind"].help_text = _(
            "Auto-detected from the file extension on sync when possible.",
        )

    def clean_github_url(self) -> str:
        from .github import GitHubFetchError
        from .github import parse_github_url

        url = (self.cleaned_data.get("github_url") or "").strip()
        try:
            ref = parse_github_url(url)
        except GitHubFetchError as exc:
            raise ValidationError(str(exc)) from exc
        return ref.html_url

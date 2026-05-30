from __future__ import annotations

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from slugify import slugify

from .models import HANDLE_MAX_LENGTH
from .models import HANDLE_MIN_LENGTH
from .models import Profile
from .models import ProjectLink
from .models import SocialLink


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
            "pronouns",
            "years_experience",
            "tech_stack",
            "avatar",
            "website_url",
            "show_email",
            "available_for_hire",
            "is_public",
        )
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 6, "placeholder": "$ cat about.md"}),
            "headline": forms.TextInput(attrs={"placeholder": "Senior Backend Engineer · Python & Go"}),
            "tech_stack": forms.TextInput(attrs={"placeholder": "python, django, postgres, aws"}),
            "handle": forms.TextInput(attrs={"placeholder": "your-handle"}),
        }

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
        if Profile.objects.exclude(pk=self.instance.pk).filter(handle=normalized).exists():
            err = _("That handle is already taken.")
            raise ValidationError(err)
        return normalized


class ProjectLinkForm(forms.ModelForm):
    class Meta:
        model = ProjectLink
        fields = (
            "title",
            "description",
            "url",
            "repo_url",
            "tech_stack",
            "is_featured",
            "order",
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
        fields = ("platform", "label", "url", "order")
        widgets = {
            "url": forms.TextInput(attrs={"placeholder": "https://github.com/your-handle"}),
            "label": forms.TextInput(attrs={"placeholder": "Optional display name"}),
        }

    def clean_url(self) -> str:
        url = (self.cleaned_data.get("url") or "").strip()
        platform = self.cleaned_data.get("platform")
        if platform == "email":
            if "@" not in url:
                err = _("Enter a valid email address.")
                raise ValidationError(err)
            if not url.lower().startswith("mailto:"):
                url = f"mailto:{url}"
            return url
        validator = forms.URLField()
        try:
            url = validator.clean(url)
        except ValidationError as exc:
            raise ValidationError(_("Enter a valid URL.")) from exc
        return url

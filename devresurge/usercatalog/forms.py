# myapp/forms.py
from django import forms

from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "profilename",
            "display_name",
            "bio",
            "location",
            "tags",
            "github_url",
            "linkedin_url",
        ]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
        }

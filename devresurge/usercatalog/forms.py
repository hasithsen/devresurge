# myapp/forms.py
from django import forms

from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "profilename",
            "display_name",
            "location",
            "tags",
            "linkedin_url",
        ]

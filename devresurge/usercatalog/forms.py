# myapp/forms.py
from django import forms

from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "profile_picture",
            "profilename",
            "display_name",
            "bio",
            "location",
            "tags",
        ]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
        }

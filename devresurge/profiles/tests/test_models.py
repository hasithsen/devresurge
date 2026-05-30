from __future__ import annotations

import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from devresurge.profiles.forms import ProfileForm
from devresurge.profiles.models import MAX_AVATAR_BYTES
from devresurge.profiles.models import Profile
from devresurge.profiles.models import validate_avatar_size
from devresurge.profiles.tests.factories import ProfileFactory
from devresurge.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_profile_created_on_user_signup():
    user = UserFactory(email="signup@example.com")
    assert Profile.objects.filter(user=user).exists()


def test_handle_is_auto_generated_when_blank():
    user = UserFactory(email="zephyr@example.com", name="Zephyr Smith")
    profile = user.profile
    profile.handle = ""
    profile.display_name = "Zephyr Smith"
    profile.save()
    assert profile.handle == "zephyr-smith"


def test_handle_collisions_get_a_numeric_suffix():
    ProfileFactory(handle="taken")
    other = ProfileFactory(handle="")
    other.display_name = "Taken"
    other.handle = ""
    other.save()
    assert other.handle.startswith("taken")
    assert other.handle != "taken"


def test_tech_stack_list_parses_csv():
    profile = ProfileFactory(tech_stack="python, django,  postgres ,,")
    assert profile.tech_stack_list == ["python", "django", "postgres"]


def test_get_absolute_url_uses_handle():
    profile = ProfileFactory(handle="hello-world")
    assert profile.get_absolute_url() == "/u/hello-world/"


def test_validate_avatar_size_rejects_oversized_files():
    fake = SimpleUploadedFile(
        "huge.png",
        b"x" * (MAX_AVATAR_BYTES + 1),
        content_type="image/png",
    )
    with pytest.raises(ValidationError):
        validate_avatar_size(fake)


def test_validate_avatar_size_accepts_small_files():
    fake = SimpleUploadedFile("tiny.png", b"x" * 1024, content_type="image/png")
    validate_avatar_size(fake)  # does not raise


def test_validate_avatar_size_accepts_none():
    validate_avatar_size(None)  # does not raise


def test_profile_form_rejects_oversized_avatar():
    user = UserFactory()
    profile = user.profile
    huge = SimpleUploadedFile(
        "x.png",
        b"x" * (MAX_AVATAR_BYTES + 1024),
        content_type="image/png",
    )
    form = ProfileForm(
        data={
            "handle": "valid-handle",
            "display_name": "X",
            "headline": "",
            "primary_role": "other",
            "bio": "",
            "location": "",
            "years_experience": 0,
            "tech_stack": "",
            "website_url": "",
        },
        files={"avatar": huge},
        instance=profile,
    )
    assert not form.is_valid()
    assert "avatar" in form.errors


def test_profile_form_rejects_unsupported_image_mime():
    user = UserFactory()
    profile = user.profile
    bad = SimpleUploadedFile(
        "x.svg",
        b"<svg></svg>",
        content_type="image/svg+xml",
    )
    form = ProfileForm(
        data={
            "handle": "valid-handle",
            "display_name": "X",
            "headline": "",
            "primary_role": "other",
            "bio": "",
            "location": "",
            "years_experience": 0,
            "tech_stack": "",
            "website_url": "",
        },
        files={"avatar": bad},
        instance=profile,
    )
    assert not form.is_valid()
    assert "avatar" in form.errors

from __future__ import annotations

import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.db import transaction

from devresurge.profiles.forms import ProfileForm
from devresurge.profiles.models import MAX_AVATAR_BYTES
from devresurge.profiles.models import Profile
from devresurge.profiles.models import validate_avatar_size
from devresurge.profiles.tests.factories import ProfileFactory
from devresurge.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def _profile_form_data(**overrides) -> dict:
    data = {
        "handle": "valid-handle",
        "display_name": "X",
        "headline": "",
        "primary_role": "other",
        "bio": "",
        "location": "",
        "years_experience": 0,
        "tech_stack": "",
        "website_url": "",
    }
    data.update(overrides)
    return data


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


# ---------------------------------------------------------------------------
# Case-insensitive handles
# ---------------------------------------------------------------------------


def test_normalize_handle_lowercases_and_strips():
    assert Profile.normalize_handle("  AdaLovelace  ") == "adalovelace"
    assert Profile.normalize_handle(None) == ""


def test_handle_is_lowercased_on_save():
    profile = ProfileFactory(handle="MixedCase")
    assert profile.handle == "mixedcase"
    profile.refresh_from_db()
    assert profile.handle == "mixedcase"


def test_handle_case_insensitive_uniqueness_enforced_in_db():
    ProfileFactory(handle="Ada")
    with pytest.raises(IntegrityError), transaction.atomic():
        ProfileFactory(handle="ada")


def test_auto_generated_handle_avoids_case_variant_collision():
    ProfileFactory(handle="Taken")
    other = ProfileFactory(handle="")
    other.display_name = "TAKEN"
    other.handle = ""
    other.save()
    assert other.handle != "taken"
    assert other.handle.startswith("taken")


def test_form_rejects_case_variant_of_existing_handle():
    ProfileFactory(handle="ada")
    user = UserFactory()
    form = ProfileForm(
        data=_profile_form_data(handle="ADA"),
        instance=user.profile,
    )
    assert not form.is_valid()
    assert "handle" in form.errors


def test_form_normalizes_handle_to_lowercase():
    user = UserFactory()
    form = ProfileForm(
        data=_profile_form_data(handle="CamelCase"),
        instance=user.profile,
    )
    assert form.is_valid(), form.errors
    assert form.cleaned_data["handle"] == "camelcase"


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


def test_readiness_scores_incomplete_profile():
    profile = ProfileFactory(
        display_name="",
        headline="",
        bio="",
        tech_stack="",
        website_url="",
        is_public=False,
        avatar=None,
    )
    readiness = profile.readiness()
    assert readiness["complete"] is False
    assert readiness["done"] < readiness["total"]
    keys = {c["key"] for c in readiness["checks"] if not c["done"]}
    assert "display_name" in keys
    assert "public" in keys
    assert "practice" in keys
    assert "tools" in keys


def test_readiness_complete_when_fully_filled():
    # Minimal valid 1×1 PNG so ImageField/Pillow accepts the avatar.
    png = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
        b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01"
        b"\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    profile = ProfileFactory(
        display_name="Full Dev",
        headline="Ships things",
        bio="About me",
        tech_stack="python",
        website_url="https://example.com",
        is_public=True,
    )
    profile.avatar.save(
        "a.png",
        SimpleUploadedFile("a.png", png, content_type="image/png"),
        save=True,
    )
    from devresurge.profiles.models import WorkExperience
    from devresurge.profiles.tests.factories import ProfileToolFactory
    from devresurge.profiles.tests.factories import ProjectLinkFactory
    from devresurge.profiles.tests.factories import ShowcaseItemFactory
    from devresurge.profiles.tests.factories import SocialLinkFactory

    ProjectLinkFactory(profile=profile)
    ProfileToolFactory(profile=profile, name="Kubernetes")
    ShowcaseItemFactory(profile=profile, is_published=True)
    SocialLinkFactory(profile=profile, platform="linkedin", url="https://linkedin.com/in/x")
    SocialLinkFactory(
        profile=profile,
        platform="leetcode",
        url="https://leetcode.com/u/fulldev/",
    )
    WorkExperience.objects.create(
        profile=profile,
        title="Engineer",
        company="Acme",
        start_year=2020,
        start_month=1,
        is_current=True,
    )
    readiness = profile.readiness()
    assert readiness["complete"] is True
    assert readiness["pct"] == 100
    assert "practice" not in {c["key"] for c in readiness["checks"] if not c["done"]}


def test_to_readme_markdown_includes_core_sections():
    profile = ProfileFactory(
        display_name="Ada",
        headline="Mathematician",
        bio="First programmer.",
        tech_stack="math, analysis",
        available_for_hire=True,
        location="London",
    )
    from devresurge.profiles.tests.factories import ProfileToolFactory
    from devresurge.profiles.tests.factories import ProjectLinkFactory
    from devresurge.profiles.tests.factories import SocialLinkFactory

    ProjectLinkFactory(profile=profile, title="Analytical Engine", is_featured=True)
    ProfileToolFactory(
        profile=profile,
        name="Analytical Engine",
        category="languages",
        note="Difference engine companion",
    )
    ProfileToolFactory(
        profile=profile,
        name="Difference Engine desk",
        category="devices",
        note="Brass & iron",
    )
    SocialLinkFactory(
        profile=profile,
        platform="leetcode",
        url="https://leetcode.com/u/ada/",
    )
    SocialLinkFactory(
        profile=profile,
        platform="github",
        url="https://github.com/ada",
    )
    md = profile.to_readme_markdown(base_url="https://devresurge.test")
    assert "# Ada" in md
    assert f"**@{profile.handle}**" in md
    assert "## Stack" in md
    assert "## Tools" in md
    assert "## Setup" in md
    assert "Analytical Engine" in md
    assert "Difference Engine desk" in md
    assert "## Projects" in md
    assert "## Practice" in md
    assert "leetcode.com/u/ada" in md
    assert "## Links" in md
    assert "github.com/ada" in md
    assert "open to work" in md
    assert "https://devresurge.test" in md


def test_tools_grouped_by_category():
    profile = ProfileFactory()
    from devresurge.profiles.models import ToolCategory
    from devresurge.profiles.tests.factories import ProfileToolFactory

    ProfileToolFactory(profile=profile, name="Docker", category=ToolCategory.INFRA, order=0)
    ProfileToolFactory(profile=profile, name="Python", category=ToolCategory.LANGUAGES, order=1)
    ProfileToolFactory(profile=profile, name="Kubernetes", category=ToolCategory.INFRA, order=2)
    ProfileToolFactory(
        profile=profile,
        name="MacBook Pro",
        category=ToolCategory.DEVICES,
        order=3,
    )
    ProfileToolFactory(
        profile=profile,
        name="Keychron K2",
        category=ToolCategory.PERIPHERALS,
        order=4,
    )
    software = profile.software_tools_grouped()
    devices = profile.device_tools_grouped()
    assert [g["category"] for g in software] == [ToolCategory.INFRA, ToolCategory.LANGUAGES]
    assert [t.name for t in software[0]["tools"]] == ["Docker", "Kubernetes"]
    assert [g["category"] for g in devices] == [ToolCategory.DEVICES, ToolCategory.PERIPHERALS]
    assert devices[0]["tools"][0].name == "MacBook Pro"


def test_practice_links_split_from_network_links():
    profile = ProfileFactory()
    from devresurge.profiles.tests.factories import SocialLinkFactory

    practice = SocialLinkFactory(
        profile=profile,
        platform="hackerrank",
        url="https://www.hackerrank.com/profile/x",
    )
    network = SocialLinkFactory(
        profile=profile,
        platform="linkedin",
        url="https://linkedin.com/in/x",
    )
    assert practice in profile.practice_links()
    assert network not in profile.practice_links()
    assert network in profile.network_links()
    assert practice not in profile.network_links()

from __future__ import annotations

import json
from http import HTTPStatus

import pytest
from django.urls import reverse

from devresurge.profiles.models import ProjectLink
from devresurge.profiles.models import SocialLink
from devresurge.profiles.tests.factories import ProfileFactory
from devresurge.profiles.tests.factories import ProjectLinkFactory
from devresurge.profiles.tests.factories import SocialLinkFactory
from devresurge.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_home_view_renders(client):
    response = client.get(reverse("home"))
    assert response.status_code == HTTPStatus.OK


def test_browse_lists_public_profiles(client):
    public = ProfileFactory(is_public=True, display_name="Public Dev")
    private = ProfileFactory(is_public=False, display_name="Private Dev")
    response = client.get(reverse("profiles:browse"))
    assert response.status_code == HTTPStatus.OK
    body = response.content.decode()
    assert public.handle in body
    assert private.handle not in body


def test_browse_search_filters_by_query(client):
    needle = ProfileFactory(display_name="Needle", tech_stack="rust, wasm")
    ProfileFactory(display_name="Haystack", tech_stack="python")
    response = client.get(reverse("profiles:browse"), {"q": "wasm"})
    body = response.content.decode()
    assert needle.handle in body


def test_public_profile_view_returns_for_public_profile(client):
    profile = ProfileFactory(is_public=True)
    response = client.get(reverse("profiles:public", kwargs={"handle": profile.handle}))
    assert response.status_code == HTTPStatus.OK


def test_public_profile_view_404s_when_private_and_not_owner(client):
    profile = ProfileFactory(is_public=False)
    response = client.get(reverse("profiles:public", kwargs={"handle": profile.handle}))
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_public_profile_canonical_url_renders_directly(client):
    ProfileFactory(is_public=True, handle="ada")
    response = client.get("/u/ada/")
    assert response.status_code == HTTPStatus.OK


def test_public_profile_mixed_case_redirects_to_canonical(client):
    ProfileFactory(is_public=True, handle="ada")
    response = client.get("/u/ADA/")
    assert response.status_code == HTTPStatus.MOVED_PERMANENTLY
    assert response.headers["Location"] == "/u/ada/"


def test_public_profile_mixed_case_resolves_when_followed(client):
    ProfileFactory(is_public=True, handle="ada", display_name="Ada L.")
    response = client.get("/u/Ada/", follow=True)
    assert response.status_code == HTTPStatus.OK
    assert b"Ada L." in response.content


def test_public_profile_unknown_handle_404s(client):
    response = client.get("/u/nobody-here/")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_dashboard_requires_login(client):
    response = client.get(reverse("profiles:dashboard"))
    assert response.status_code == HTTPStatus.FOUND
    assert "/accounts/login/" in response.url


def test_dashboard_renders_for_owner(client):
    user = UserFactory(password="pass1234!")
    client.force_login(user)
    response = client.get(reverse("profiles:dashboard"))
    assert response.status_code == HTTPStatus.OK


def test_edit_profile_persists_changes(client):
    user = UserFactory()
    client.force_login(user)
    profile = user.profile
    response = client.post(
        reverse("profiles:edit"),
        data={
            "handle": "polaris",
            "display_name": "Polaris",
            "headline": "Backend wrangler",
            "primary_role": "backend",
            "bio": "I write servers.",
            "location": "Colombo",
            "years_experience": 5,
            "tech_stack": "python, django",
            "website_url": "",
            "show_email": "on",
            "available_for_hire": "on",
            "is_public": "on",
        },
    )
    assert response.status_code == HTTPStatus.FOUND
    profile.refresh_from_db()
    assert profile.handle == "polaris"
    assert profile.display_name == "Polaris"
    assert profile.primary_role == "backend"


def test_project_link_create_attaches_to_profile(client):
    user = UserFactory()
    client.force_login(user)
    response = client.post(
        reverse("profiles:project_create"),
        data={
            "title": "Cool tool",
            "description": "Does cool things.",
            "url": "https://example.com",
            "repo_url": "",
            "tech_stack": "python",
            "is_featured": "on",
            "order": 0,
        },
    )
    assert response.status_code == HTTPStatus.FOUND
    assert ProjectLink.objects.filter(profile__user=user, title="Cool tool").exists()


def test_project_link_requires_url_or_repo(client):
    user = UserFactory()
    client.force_login(user)
    response = client.post(
        reverse("profiles:project_create"),
        data={
            "title": "Bad",
            "description": "",
            "url": "",
            "repo_url": "",
            "tech_stack": "",
            "is_featured": "",
            "order": 0,
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert not ProjectLink.objects.filter(title="Bad").exists()


def test_social_link_create_and_owner_scoped_edit(client):
    user = UserFactory()
    client.force_login(user)
    client.post(
        reverse("profiles:link_create"),
        data={"platform": "github", "label": "gh", "url": "https://github.com/me", "order": 0},
    )
    link = SocialLink.objects.get(profile__user=user)

    other = UserFactory()
    client.force_login(other)
    response = client.get(reverse("profiles:link_update", kwargs={"pk": link.pk}))
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_social_link_email_is_normalized_to_mailto(client):
    user = UserFactory()
    client.force_login(user)
    response = client.post(
        reverse("profiles:link_create"),
        data={"platform": "email", "label": "mail", "url": "hi@example.com", "order": 0},
    )
    assert response.status_code == HTTPStatus.FOUND
    link = SocialLink.objects.get(profile__user=user, platform="email")
    assert link.url == "mailto:hi@example.com"


# ---------------------------------------------------------------------------
# Drag-and-drop reorder endpoints
# ---------------------------------------------------------------------------


def test_project_reorder_requires_login(client):
    response = client.post(
        reverse("profiles:project_reorder"),
        data=json.dumps({"ids": [1, 2]}),
        content_type="application/json",
    )
    assert response.status_code == HTTPStatus.FOUND


def test_project_reorder_rejects_get(client):
    user = UserFactory()
    client.force_login(user)
    response = client.get(reverse("profiles:project_reorder"))
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED


def test_project_reorder_persists_new_order(client):
    user = UserFactory()
    client.force_login(user)
    profile = user.profile
    a = ProjectLinkFactory(profile=profile, title="A", order=0)
    b = ProjectLinkFactory(profile=profile, title="B", order=1)
    c = ProjectLinkFactory(profile=profile, title="C", order=2)

    response = client.post(
        reverse("profiles:project_reorder"),
        data=json.dumps({"ids": [c.pk, a.pk, b.pk]}),
        content_type="application/json",
    )
    assert response.status_code == HTTPStatus.OK
    payload = response.json()
    assert payload["ok"] is True
    assert payload["updated"] == 3

    titles = list(profile.projects.order_by("order").values_list("title", flat=True))
    assert titles == ["C", "A", "B"]


def test_project_reorder_ignores_foreign_ids(client):
    user = UserFactory()
    client.force_login(user)
    profile = user.profile
    mine = ProjectLinkFactory(profile=profile, title="Mine", order=0)

    other_user = UserFactory()
    foreign = ProjectLinkFactory(profile=other_user.profile, title="Theirs", order=5)

    response = client.post(
        reverse("profiles:project_reorder"),
        data=json.dumps({"ids": [foreign.pk, mine.pk]}),
        content_type="application/json",
    )
    assert response.status_code == HTTPStatus.OK
    foreign.refresh_from_db()
    mine.refresh_from_db()
    assert foreign.order == 5
    assert mine.order == 0


def test_link_reorder_persists_new_order(client):
    user = UserFactory()
    client.force_login(user)
    profile = user.profile
    a = SocialLinkFactory(profile=profile, platform="github", url="https://g/a", order=0)
    b = SocialLinkFactory(profile=profile, platform="gitlab", url="https://g/b", order=1)

    response = client.post(
        reverse("profiles:link_reorder"),
        data=json.dumps({"ids": [b.pk, a.pk]}),
        content_type="application/json",
    )
    assert response.status_code == HTTPStatus.OK
    ordered = list(profile.social_links.order_by("order").values_list("pk", flat=True))
    assert ordered == [b.pk, a.pk]


def test_reorder_handles_garbage_payload(client):
    user = UserFactory()
    client.force_login(user)
    response = client.post(
        reverse("profiles:project_reorder"),
        data="not json at all",
        content_type="application/json",
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_reorder_requires_ids_list(client):
    user = UserFactory()
    client.force_login(user)
    response = client.post(
        reverse("profiles:project_reorder"),
        data=json.dumps({"nope": "wat"}),
        content_type="application/json",
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST

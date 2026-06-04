from __future__ import annotations

import json
from datetime import timedelta
from http import HTTPStatus
from io import StringIO

import pytest
from django.core.management import call_command
from django.urls import reverse
from django.utils import timezone

from devresurge.profiles.models import LinkClick
from devresurge.profiles.models import ProfileView
from devresurge.profiles.tests.factories import ProfileFactory
from devresurge.profiles.tests.factories import ProjectLinkFactory
from devresurge.profiles.tests.factories import SocialLinkFactory
from devresurge.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def _beacon(client, **payload):
    return client.post(
        reverse("profiles:link_click"),
        data=json.dumps(payload),
        content_type="application/json",
    )


# ---------------------------------------------------------------------------
# Beacon recording
# ---------------------------------------------------------------------------


def test_beacon_records_project_click(client):
    profile = ProfileFactory(is_public=True)
    project = ProjectLinkFactory(
        profile=profile,
        url="https://example.com/app",
        repo_url="",
    )
    response = _beacon(
        client,
        handle=profile.handle,
        kind="project",
        id=project.pk,
        field="primary",
    )
    assert response.status_code == HTTPStatus.NO_CONTENT
    click = LinkClick.objects.get(profile=profile)
    assert click.kind == "project"
    assert click.target_id == project.pk
    assert click.label == project.title
    assert click.destination == "example.com"
    assert click.visitor_hash  # populated, irreversible


def test_beacon_project_repo_field_uses_repo_host(client):
    profile = ProfileFactory(is_public=True)
    project = ProjectLinkFactory(
        profile=profile,
        url="https://example.com",
        repo_url="https://github.com/me/proj",
    )
    _beacon(client, handle=profile.handle, kind="project", id=project.pk, field="repo")
    click = LinkClick.objects.get(profile=profile)
    assert click.destination == "github.com"


def test_beacon_records_social_click(client):
    profile = ProfileFactory(is_public=True)
    link = SocialLinkFactory(profile=profile, platform="github", url="https://github.com/me")
    _beacon(client, handle=profile.handle, kind="social", id=link.pk)
    click = LinkClick.objects.get(profile=profile)
    assert click.kind == "social"
    assert click.target_id == link.pk
    assert click.label == link.display_label
    assert click.destination == "github.com"


def test_beacon_records_website_click(client):
    profile = ProfileFactory(is_public=True, website_url="https://mysite.dev/")
    _beacon(client, handle=profile.handle, kind="website")
    click = LinkClick.objects.get(profile=profile)
    assert click.kind == "website"
    assert click.label == "website"
    assert click.destination == "mysite.dev"
    assert click.target_id is None


def test_beacon_records_email_click(client):
    profile = ProfileFactory(is_public=True)
    _beacon(client, handle=profile.handle, kind="email")
    click = LinkClick.objects.get(profile=profile)
    assert click.kind == "email"
    assert click.destination == "email"
    assert click.target_id is None


# ---------------------------------------------------------------------------
# Beacon guards
# ---------------------------------------------------------------------------


def test_beacon_unknown_profile_is_ignored(client):
    response = _beacon(client, handle="ghost", kind="email")
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert LinkClick.objects.count() == 0


def test_beacon_private_profile_is_ignored(client):
    profile = ProfileFactory(is_public=False)
    response = _beacon(client, handle=profile.handle, kind="email")
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert LinkClick.objects.count() == 0


def test_beacon_owner_click_is_not_tracked(client):
    user = UserFactory()
    profile = user.profile
    profile.is_public = True
    profile.save()
    client.force_login(user)
    _beacon(client, handle=profile.handle, kind="email")
    assert LinkClick.objects.count() == 0


def test_beacon_bot_user_agent_is_skipped(client):
    profile = ProfileFactory(is_public=True)
    client.post(
        reverse("profiles:link_click"),
        data=json.dumps({"handle": profile.handle, "kind": "email"}),
        content_type="application/json",
        HTTP_USER_AGENT="Googlebot/2.1 (+http://www.google.com/bot.html)",
    )
    assert LinkClick.objects.count() == 0


def test_beacon_unknown_target_is_ignored(client):
    profile = ProfileFactory(is_public=True)
    response = _beacon(client, handle=profile.handle, kind="project", id=999999)
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert LinkClick.objects.count() == 0


def test_beacon_invalid_json_returns_400(client):
    response = client.post(
        reverse("profiles:link_click"),
        data="this is not json",
        content_type="application/json",
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert LinkClick.objects.count() == 0


def test_beacon_invalid_kind_returns_400(client):
    profile = ProfileFactory(is_public=True)
    response = _beacon(client, handle=profile.handle, kind="bogus")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert LinkClick.objects.count() == 0


def test_beacon_requires_post(client):
    response = client.get(reverse("profiles:link_click"))
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED


def test_beacon_dedupes_rapid_duplicate_clicks(client):
    profile = ProfileFactory(is_public=True)
    _beacon(client, handle=profile.handle, kind="email")
    _beacon(client, handle=profile.handle, kind="email")
    assert LinkClick.objects.filter(profile=profile).count() == 1


# ---------------------------------------------------------------------------
# Analytics aggregation
# ---------------------------------------------------------------------------


def test_analytics_reports_clicks(client):
    user = UserFactory()
    profile = user.profile
    for _ in range(3):
        LinkClick.objects.create(
            profile=profile,
            kind="social",
            label="github",
            destination="github.com",
            visitor_hash="v",
        )
    LinkClick.objects.create(
        profile=profile,
        kind="website",
        label="website",
        destination="mysite.dev",
        visitor_hash="v",
    )

    client.force_login(user)
    response = client.get(reverse("profiles:analytics"))
    assert response.context["total_clicks"] == 4
    assert response.context["has_clicks"] is True
    top = response.context["top_links"]
    assert top[0]["count"] == 3
    assert top[0]["destination"] == "github.com"


def test_analytics_has_data_when_only_clicks_present(client):
    user = UserFactory()
    LinkClick.objects.create(
        profile=user.profile,
        kind="email",
        label="email",
        destination="email",
        visitor_hash="v",
    )
    client.force_login(user)
    response = client.get(reverse("profiles:analytics"))
    assert response.context["has_views"] is False
    assert response.context["has_clicks"] is True
    assert response.context["has_data"] is True


# ---------------------------------------------------------------------------
# Retention / pruning
# ---------------------------------------------------------------------------


def _backdate(click, days):
    LinkClick.objects.filter(pk=click.pk).update(
        created_at=timezone.now() - timedelta(days=days),
    )


def test_link_click_prune_deletes_only_old_rows():
    profile = ProfileFactory()
    fresh = LinkClick.objects.create(profile=profile, kind="email", visitor_hash="f")
    stale = LinkClick.objects.create(profile=profile, kind="email", visitor_hash="s")
    _backdate(stale, 120)

    deleted = LinkClick.prune()
    assert deleted == 1
    assert LinkClick.objects.filter(pk=fresh.pk).exists()
    assert not LinkClick.objects.filter(pk=stale.pk).exists()


def test_prune_command_prunes_both_models():
    profile = ProfileFactory()
    stale_view = ProfileView.objects.create(profile=profile, visitor_hash="v")
    stale_click = LinkClick.objects.create(profile=profile, kind="email", visitor_hash="c")
    ProfileView.objects.filter(pk=stale_view.pk).update(
        created_at=timezone.now() - timedelta(days=100),
    )
    _backdate(stale_click, 100)

    out = StringIO()
    call_command("prune_analytics", stdout=out)
    output = out.getvalue()
    assert "link click" in output
    assert "Total: 2" in output
    assert ProfileView.objects.count() == 0
    assert LinkClick.objects.count() == 0

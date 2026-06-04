from __future__ import annotations

from datetime import timedelta
from http import HTTPStatus
from io import StringIO

import pytest
from django.core.management import call_command
from django.urls import reverse
from django.utils import timezone

from devresurge.profiles.models import ProfileView
from devresurge.profiles.tests.factories import ProfileFactory
from devresurge.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


# ---------------------------------------------------------------------------
# View recording
# ---------------------------------------------------------------------------


def test_public_view_records_event_for_anonymous_visitor(client):
    profile = ProfileFactory(is_public=True)
    client.get(reverse("profiles:public", kwargs={"handle": profile.handle}))
    assert ProfileView.objects.filter(profile=profile).count() == 1
    event = ProfileView.objects.get(profile=profile)
    assert event.is_unique is True
    assert event.visitor_hash  # populated, irreversible


def test_repeat_visit_same_day_is_not_unique(client):
    profile = ProfileFactory(is_public=True)
    url = reverse("profiles:public", kwargs={"handle": profile.handle})
    client.get(url)
    client.get(url)
    events = ProfileView.objects.filter(profile=profile)
    assert events.count() == 2
    assert events.filter(is_unique=True).count() == 1
    # Same fingerprint → one unique visitor.
    assert events.values("visitor_hash").distinct().count() == 1


def test_owner_viewing_own_profile_is_not_counted(client):
    user = UserFactory()
    profile = user.profile
    profile.is_public = True
    profile.save()
    client.force_login(user)
    client.get(reverse("profiles:public", kwargs={"handle": profile.handle}))
    assert ProfileView.objects.filter(profile=profile).count() == 0


def test_private_profile_404_records_nothing(client):
    profile = ProfileFactory(is_public=False)
    response = client.get(reverse("profiles:public", kwargs={"handle": profile.handle}))
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert ProfileView.objects.filter(profile=profile).count() == 0


def test_bot_user_agent_is_skipped(client):
    profile = ProfileFactory(is_public=True)
    client.get(
        reverse("profiles:public", kwargs={"handle": profile.handle}),
        HTTP_USER_AGENT="Googlebot/2.1 (+http://www.google.com/bot.html)",
    )
    assert ProfileView.objects.filter(profile=profile).count() == 0


def test_external_referrer_is_captured(client):
    profile = ProfileFactory(is_public=True)
    client.get(
        reverse("profiles:public", kwargs={"handle": profile.handle}),
        HTTP_REFERER="https://news.ycombinator.com/item?id=1",
    )
    event = ProfileView.objects.get(profile=profile)
    assert event.referrer == "news.ycombinator.com"


# ---------------------------------------------------------------------------
# Analytics dashboard view
# ---------------------------------------------------------------------------


def test_analytics_requires_login(client):
    response = client.get(reverse("profiles:analytics"))
    assert response.status_code == HTTPStatus.FOUND
    assert "/accounts/login/" in response.url


def test_analytics_renders_for_owner(client):
    user = UserFactory()
    client.force_login(user)
    response = client.get(reverse("profiles:analytics"))
    assert response.status_code == HTTPStatus.OK
    assert b"analytics" in response.content.lower()


def test_analytics_counts_views_in_window(client):
    user = UserFactory()
    profile = user.profile
    for _ in range(3):
        ProfileView.objects.create(profile=profile, visitor_hash="abc", is_unique=False)
    ProfileView.objects.create(profile=profile, visitor_hash="def", is_unique=True)

    client.force_login(user)
    response = client.get(reverse("profiles:analytics"))
    assert response.context["total_views"] == 4
    assert response.context["unique_visitors"] == 2
    assert response.context["has_data"] is True


def test_analytics_range_defaults_and_validates(client):
    user = UserFactory()
    client.force_login(user)

    default = client.get(reverse("profiles:analytics"))
    assert default.context["days"] == 30

    valid = client.get(reverse("profiles:analytics"), {"days": 7})
    assert valid.context["days"] == 7

    invalid = client.get(reverse("profiles:analytics"), {"days": 9999})
    assert invalid.context["days"] == 30

    garbage = client.get(reverse("profiles:analytics"), {"days": "abc"})
    assert garbage.context["days"] == 30


def test_analytics_excludes_events_outside_window(client):
    user = UserFactory()
    profile = user.profile
    old = ProfileView.objects.create(profile=profile, visitor_hash="old", is_unique=True)
    ProfileView.objects.filter(pk=old.pk).update(
        created_at=timezone.now() - timedelta(days=45),
    )

    client.force_login(user)
    response = client.get(reverse("profiles:analytics"), {"days": 7})
    assert response.context["total_views"] == 0
    assert response.context["has_data"] is False


# ---------------------------------------------------------------------------
# Retention / pruning
# ---------------------------------------------------------------------------


def _backdate(event, days):
    ProfileView.objects.filter(pk=event.pk).update(
        created_at=timezone.now() - timedelta(days=days),
    )


def test_prune_deletes_only_old_events():
    profile = ProfileFactory()
    fresh = ProfileView.objects.create(profile=profile, visitor_hash="fresh")
    stale = ProfileView.objects.create(profile=profile, visitor_hash="stale")
    _backdate(stale, 120)

    deleted = ProfileView.prune()
    assert deleted == 1
    assert ProfileView.objects.filter(pk=fresh.pk).exists()
    assert not ProfileView.objects.filter(pk=stale.pk).exists()


def test_prune_respects_custom_days():
    profile = ProfileFactory()
    event = ProfileView.objects.create(profile=profile, visitor_hash="x")
    _backdate(event, 10)

    assert ProfileView.prune(days=30) == 0
    assert ProfileView.prune(days=7) == 1


def test_prune_analytics_command_deletes_old_rows():
    profile = ProfileFactory()
    stale = ProfileView.objects.create(profile=profile, visitor_hash="stale")
    _backdate(stale, 100)

    out = StringIO()
    call_command("prune_analytics", stdout=out)
    assert "Deleted 1" in out.getvalue()
    assert ProfileView.objects.count() == 0


def test_prune_analytics_command_dry_run_keeps_rows():
    profile = ProfileFactory()
    stale = ProfileView.objects.create(profile=profile, visitor_hash="stale")
    _backdate(stale, 100)

    out = StringIO()
    call_command("prune_analytics", "--dry-run", stdout=out)
    assert "dry-run" in out.getvalue()
    assert ProfileView.objects.count() == 1

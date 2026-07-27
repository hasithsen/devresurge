from __future__ import annotations

from http import HTTPStatus

import pytest
from django.urls import reverse

from devresurge.connections.models import Connection
from devresurge.connections.models import ConnectionStatus
from devresurge.connections.models import Notification
from devresurge.connections.models import NotificationKind
from devresurge.profiles.models import Recommendation
from devresurge.profiles.models import SkillEndorsement
from devresurge.profiles.models import WorkExperience
from devresurge.profiles.tests.factories import ProfileFactory
from devresurge.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def _connect(a, b):
    return Connection.objects.create(
        requester=a,
        addressee=b,
        status=ConnectionStatus.ACCEPTED,
    )


def test_experience_create(client):
    user = UserFactory()
    client.force_login(user)
    response = client.post(
        reverse("profiles:experience_create"),
        data={
            "title": "Backend Engineer",
            "company": "Acme",
            "location": "Remote",
            "description": "Built APIs.",
            "start_year": 2021,
            "start_month": 3,
            "is_current": "on",
        },
    )
    assert response.status_code == HTTPStatus.FOUND
    exp = WorkExperience.objects.get(profile__user=user)
    assert exp.title == "Backend Engineer"
    assert exp.is_current is True


def test_browse_intent_collaborate(client):
    match = ProfileFactory(is_public=True, open_to_collaborate=True, display_name="Collab Dev")
    other = ProfileFactory(is_public=True, open_to_collaborate=False, display_name="Solo Dev")
    response = client.get(reverse("profiles:browse"), {"intent": "collaborate"})
    body = response.content.decode()
    assert match.handle in body
    assert other.handle not in body


def test_endorse_requires_connection(client):
    owner = UserFactory()
    owner.profile.tech_stack = "python, django"
    owner.profile.is_public = True
    owner.profile.save()
    viewer = UserFactory()
    client.force_login(viewer)
    response = client.post(
        reverse("profiles:endorse", kwargs={"handle": owner.profile.handle}),
        data={"skill": "python"},
    )
    assert response.status_code == HTTPStatus.FOUND
    assert SkillEndorsement.objects.count() == 0


def test_endorse_from_connection(client):
    owner = UserFactory()
    owner.profile.tech_stack = "python, django"
    owner.profile.is_public = True
    owner.profile.save()
    viewer = UserFactory()
    _connect(viewer, owner)
    client.force_login(viewer)
    response = client.post(
        reverse("profiles:endorse", kwargs={"handle": owner.profile.handle}),
        data={"skill": "python"},
    )
    assert response.status_code == HTTPStatus.FOUND
    assert SkillEndorsement.objects.filter(
        profile=owner.profile,
        endorser=viewer,
        skill="python",
    ).exists()
    assert Notification.objects.filter(
        recipient=owner,
        kind=NotificationKind.SKILL_ENDORSED,
    ).exists()


def test_recommendation_from_connection(client):
    owner = UserFactory()
    owner.profile.is_public = True
    owner.profile.save()
    viewer = UserFactory()
    _connect(viewer, owner)
    client.force_login(viewer)
    body = "A" * 50
    response = client.post(
        reverse("profiles:recommend", kwargs={"handle": owner.profile.handle}),
        data={"relationship": "Teammate", "body": body},
    )
    assert response.status_code == HTTPStatus.FOUND
    rec = Recommendation.objects.get(profile=owner.profile, author=viewer)
    assert rec.body == body
    public = client.get(reverse("profiles:public", kwargs={"handle": owner.profile.handle}))
    assert body.encode() in public.content

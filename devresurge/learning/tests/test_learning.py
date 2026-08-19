from http import HTTPStatus

import pytest
from django.urls import reverse

from devresurge.learning.catalog import all_roadmaps
from devresurge.learning.catalog import get_roadmap
from devresurge.learning.catalog import lesson_count
from devresurge.learning.catalog import roadmap_count
from devresurge.learning.flavor import FLAVOR
from devresurge.learning.models import LessonProgress
from devresurge.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_catalog_has_expected_roadmaps():
    assert roadmap_count() >= 8
    assert lesson_count() >= 40
    elite = get_roadmap("elite-engineer-path")
    assert elite is not None
    assert elite.lessons
    foundations = get_roadmap("strong-foundations")
    assert foundations is not None


def test_every_lesson_has_flavor():
    missing = []
    for roadmap in all_roadmaps():
        for lesson in roadmap.lessons:
            if lesson.slug not in FLAVOR:
                missing.append(lesson.slug)
            assert lesson.hook
            assert lesson.boss_fight
            assert lesson.xp > 0
    assert missing == []


def test_roadmap_list_ok(client):
    response = client.get(reverse("learning:list"))
    assert response.status_code == HTTPStatus.OK
    assert b"learn" in response.content.lower()
    assert b"elite" in response.content.lower()
    assert b"sign in to start" in response.content.lower()


def test_lesson_requires_login(client):
    roadmap = get_roadmap("elite-engineer-path")
    lesson = roadmap.lessons[0]
    url = reverse(
        "learning:lesson",
        kwargs={"roadmap_slug": roadmap.slug, "lesson_slug": lesson.slug},
    )
    response = client.get(url)
    assert response.status_code == HTTPStatus.FOUND
    assert "/accounts/login/" in response.url


def test_lesson_saves_started_progress(client):
    user = UserFactory()
    client.force_login(user)
    roadmap = get_roadmap("elite-engineer-path")
    lesson = roadmap.lessons[0]
    url = reverse(
        "learning:lesson",
        kwargs={"roadmap_slug": roadmap.slug, "lesson_slug": lesson.slug},
    )
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert lesson.title.encode() in response.content
    assert lesson.hook.encode() in response.content
    progress = LessonProgress.objects.get(
        user=user,
        roadmap_slug=roadmap.slug,
        lesson_slug=lesson.slug,
    )
    assert progress.status == LessonProgress.Status.STARTED


def test_clearing_lesson_saves_and_advances(client):
    user = UserFactory()
    client.force_login(user)
    roadmap = get_roadmap("elite-engineer-path")
    first, second = roadmap.lessons[0], roadmap.lessons[1]
    url = reverse(
        "learning:complete",
        kwargs={"roadmap_slug": roadmap.slug, "lesson_slug": first.slug},
    )
    response = client.post(url)
    assert response.status_code == HTTPStatus.FOUND
    assert second.slug in response.url
    progress = LessonProgress.objects.get(
        user=user,
        roadmap_slug=roadmap.slug,
        lesson_slug=first.slug,
    )
    assert progress.status == LessonProgress.Status.COMPLETED
    assert progress.completed_at is not None


def test_each_roadmap_renders(client):
    for roadmap in all_roadmaps():
        r = client.get(reverse("learning:roadmap", kwargs={"roadmap_slug": roadmap.slug}))
        assert r.status_code == HTTPStatus.OK, roadmap.slug


def test_unknown_roadmap_404(client):
    response = client.get(reverse("learning:roadmap", kwargs={"roadmap_slug": "nope"}))
    assert response.status_code == HTTPStatus.NOT_FOUND

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


def test_lesson_appends_official_reference_links():
    elective = get_roadmap("relocation-sweden")
    assert elective is not None
    visa = elective.get_lesson("reloc-se-visa")
    assert visa is not None
    assert "migrationsverket" in visa.body.lower()
    devops = get_roadmap("devops-interview")
    assert devops is not None
    assert devops.track == "interview"
    assert "relocation-sweden" in devops.related_roadmap_slugs


def test_devops_interview_sprint_is_faang_bar():
    devops = get_roadmap("devops-interview")
    assert devops is not None
    assert devops.lesson_count >= 20
    combined = " ".join(lesson.body.lower() for lesson in devops.lessons)
    assert "volvo" not in combined
    assert "slo" in combined or "error budget" in combined
    assert devops.get_lesson("cicd-release-engineering") is not None
    assert devops.get_lesson("cloud-platform-engineering") is not None
    assert "system-design-basics" in devops.related_quiz_slugs


def test_slug_aliases_resolve():
    assert get_roadmap("devops-interview-30-day") is not None
    assert get_roadmap("devops-interview-30-day").slug == "devops-interview"
    assert get_roadmap("qa-interview-sweden") is not None
    assert get_roadmap("qa-interview-sweden").slug == "relocation-sweden"


def test_sponsor_employer_paths():
    sweden = get_roadmap("sponsor-employers-sweden")
    assert sweden is not None
    assert sweden.track == "sponsor"
    assert sweden.get_lesson("sp-se-volvo-ecosystem") is not None
    assert sweden.get_lesson("sp-se-ifs-platform") is not None
    australia = get_roadmap("sponsor-employers-australia")
    assert australia.get_lesson("sp-au-ifs-platform") is not None
    usa = get_roadmap("sponsor-employers-usa")
    assert usa.get_lesson("sp-us-ifs-platform") is not None
    assert get_roadmap("volvo-sponsor-path") is not None
    assert get_roadmap("volvo-sponsor-path").slug == "sponsor-employers-sweden"
    reloc_se = get_roadmap("relocation-sweden")
    assert "sponsor-employers-sweden" in reloc_se.related_roadmap_slugs
    combined = " ".join(lesson.body.lower() for lesson in sweden.lessons)
    assert "hasith" not in combined


def test_career_roadmaps_merged_structure():
    assert get_roadmap("data-eng-interview") is not None
    assert get_roadmap("data-science-interview") is not None
    assert get_roadmap("devsecops-interview") is not None
    assert get_roadmap("data-fundamentals-elective") is not None
    assert get_roadmap("data-fundamentals-elective").track == "elective"
    assert get_roadmap("data-eng-interview-sweden") is not None
    assert get_roadmap("data-eng-interview-sweden").slug == "relocation-sweden"
    assert get_roadmap("data-science-interview-usa") is not None
    assert get_roadmap("data-science-interview-usa").slug == "relocation-usa"
    de = get_roadmap("data-eng-interview")
    assert "data-fundamentals-elective" in de.related_roadmap_slugs
    assert "data-science-interview" in de.related_roadmap_slugs
    dso = get_roadmap("devsecops-interview")
    assert "devops-interview" in dso.related_roadmap_slugs
    assert roadmap_count() >= 27
    assert roadmap_count() < 50


def test_data_fundamentals_lesson_refs():
    elective = get_roadmap("data-fundamentals-elective")
    sql = elective.get_lesson("df-sql")
    assert sql is not None
    assert "sql-fundamentals" in sql.body.lower() or "sql" in sql.body.lower()
    assert "mode.com" in sql.body.lower() or "pandas" in elective.get_lesson("df-python").body.lower()


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

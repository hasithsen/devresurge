from django.test import Client
from django.urls import reverse

from devresurge.learning.catalog import all_roadmaps
from devresurge.learning.catalog import get_roadmap
from devresurge.learning.catalog import lesson_count
from devresurge.learning.catalog import roadmap_count


def test_catalog_has_expected_roadmaps():
    assert roadmap_count() >= 8
    assert lesson_count() >= 40
    elite = get_roadmap("elite-engineer-path")
    assert elite is not None
    assert elite.lessons
    foundations = get_roadmap("strong-foundations")
    assert foundations is not None


def test_roadmap_list_ok(client: Client):
    response = client.get(reverse("learning:list"))
    assert response.status_code == 200
    assert b"learn" in response.content.lower()
    assert b"elite" in response.content.lower()


def test_each_roadmap_and_lesson_renders(client: Client):
    for roadmap in all_roadmaps():
        r = client.get(reverse("learning:roadmap", kwargs={"roadmap_slug": roadmap.slug}))
        assert r.status_code == 200, roadmap.slug
        for lesson in roadmap.lessons:
            lr = client.get(
                reverse(
                    "learning:lesson",
                    kwargs={
                        "roadmap_slug": roadmap.slug,
                        "lesson_slug": lesson.slug,
                    },
                ),
            )
            assert lr.status_code == 200, f"{roadmap.slug}/{lesson.slug}"
            assert lesson.title.encode() in lr.content


def test_unknown_roadmap_404(client: Client):
    response = client.get(reverse("learning:roadmap", kwargs={"roadmap_slug": "nope"}))
    assert response.status_code == 404

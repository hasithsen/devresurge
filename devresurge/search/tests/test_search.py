from __future__ import annotations

from http import HTTPStatus

import pytest
from django.core.cache import cache
from django.urls import reverse

from devresurge.profiles.tests.factories import ProfileFactory
from devresurge.profiles.tests.factories import ProfileToolFactory
from devresurge.quizzes.catalog import seed_catalog
from devresurge.search.courses import build_course_index
from devresurge.search.courses import clear_course_index_cache
from devresurge.search.courses import resolve_course_file
from devresurge.search.services import normalize_query
from devresurge.search.services import search


@pytest.fixture
def seeded_quizzes(db):
    seed_catalog()


@pytest.fixture(autouse=True)
def _clear_caches():
    cache.clear()
    clear_course_index_cache()
    yield
    cache.clear()
    clear_course_index_cache()


@pytest.mark.django_db
def test_normalize_query_trims_and_caps():
    assert normalize_query("  hello   world  ") == "hello world"
    assert len(normalize_query("x" * 200)) == 80


@pytest.mark.django_db
def test_search_finds_people_quizzes_courses_learn(seeded_quizzes):
    # Profile is auto-created on User save; mutate the instance so fields stick.
    public = ProfileFactory()
    public.handle = "ada-search"
    public.display_name = "Ada Lovelace"
    public.headline = "Kubernetes platform engineer"
    public.tech_stack = "python, kubernetes"
    public.is_public = True
    public.save()

    private = ProfileFactory()
    private.handle = "secret-search"
    private.display_name = "Hidden"
    private.headline = "kubernetes"
    private.is_public = False
    private.save()

    payload = search("kubernetes", per_type=10, use_cache=False)
    types = {hit["type"] for hit in payload["results"]}
    assert "people" in types
    assert "quizzes" in types or "courses" in types or "learn" in types
    handles = [
        hit["meta"].get("handle")
        for hit in payload["results"]
        if hit["type"] == "people"
    ]
    assert "ada-search" in handles
    assert "secret-search" not in handles


@pytest.mark.django_db
def test_search_api_and_page(client, seeded_quizzes):
    profile = ProfileFactory()
    profile.handle = "linus-search"
    profile.display_name = "Linus"
    profile.headline = "linux kernel"
    profile.is_public = True
    profile.save()

    api = client.get(reverse("search:api"), {"q": "linux"})
    assert api.status_code == HTTPStatus.OK
    data = api.json()
    assert data["query"] == "linux"
    assert data["total"] >= 1
    assert "Cache-Control" in api.headers

    page = client.get(reverse("search:page"), {"q": "linux"})
    assert page.status_code == HTTPStatus.OK
    assert b"linux" in page.content.lower()


@pytest.mark.django_db
def test_search_api_rate_limit(client, settings):
    settings.SEARCH_RATE_LIMIT = 2
    settings.SEARCH_RATE_WINDOW = 60
    url = reverse("search:api")
    assert client.get(url, {"q": "ab"}).status_code == HTTPStatus.OK
    assert client.get(url, {"q": "ab"}).status_code == HTTPStatus.OK
    limited = client.get(url, {"q": "ab"})
    assert limited.status_code == HTTPStatus.TOO_MANY_REQUESTS
    assert limited.json()["error"] == "rate_limited"


@pytest.mark.django_db
def test_search_rejects_short_query(client):
    response = client.get(reverse("search:api"), {"q": "a"})
    assert response.status_code == HTTPStatus.OK
    assert response.json()["total"] == 0


def test_course_index_and_path_safety():
    clear_course_index_cache()
    docs = build_course_index()
    assert any(d.course_slug == "k8s-internals" for d in docs)
    assert resolve_course_file("k8s-internals") is not None
    assert resolve_course_file("k8s-internals", "01-linux-processes") is not None
    assert resolve_course_file("../etc", "passwd") is None
    assert resolve_course_file("k8s-internals", "..") is None
    assert resolve_course_file("k8s-internals", "../../settings") is None


@pytest.mark.django_db
def test_course_viewer(client):
    listing = client.get(reverse("courses:list"))
    assert listing.status_code == HTTPStatus.OK
    assert b"k8s-internals" in listing.content or b"Kubernetes" in listing.content

    detail = client.get(reverse("courses:detail", kwargs={"course_slug": "k8s-internals"}))
    assert detail.status_code == HTTPStatus.OK

    chapter = client.get(
        reverse(
            "courses:chapter",
            kwargs={"course_slug": "k8s-internals", "chapter_slug": "01-linux-processes"},
        ),
    )
    assert chapter.status_code == HTTPStatus.OK
    assert b"process" in chapter.content.lower()

    missing = client.get(
        reverse(
            "courses:chapter",
            kwargs={"course_slug": "k8s-internals", "chapter_slug": "no-such-chapter"},
        ),
    )
    assert missing.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_search_tools(client):
    profile = ProfileFactory()
    profile.is_public = True
    profile.handle = "toolish"
    profile.save()
    ProfileToolFactory(profile=profile, name="kubectl")
    payload = search("kubectl", types=("tools",), use_cache=False)
    assert payload["total"] >= 1
    assert payload["results"][0]["type"] == "tools"

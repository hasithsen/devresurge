from __future__ import annotations

from unittest.mock import patch

import pytest
from django.urls import reverse

from devresurge.profiles.github import GitHubFetchError
from devresurge.profiles.github import companion_preview_paths
from devresurge.profiles.github import detect_kind
from devresurge.profiles.github import is_excalidraw_embed
from devresurge.profiles.github import is_excalidraw_source
from devresurge.profiles.github import parse_github_url
from devresurge.profiles.github import resolve_excalidraw_ref
from devresurge.profiles.models import ShowcaseItem
from devresurge.profiles.models import ShowcaseKind
from devresurge.profiles.tests.factories import ProfileFactory
from devresurge.profiles.tests.factories import ShowcaseItemFactory
from devresurge.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_parse_github_blob_url():
    ref = parse_github_url(
        "https://github.com/acme/lab/blob/main/designs/api.excalidraw",
    )
    assert ref.owner == "acme"
    assert ref.repo == "lab"
    assert ref.ref == "main"
    assert ref.path == "designs/api.excalidraw"
    assert "raw.githubusercontent.com/acme/lab/main/designs/api.excalidraw" in ref.raw_url


def test_parse_raw_github_url():
    ref = parse_github_url(
        "https://raw.githubusercontent.com/acme/lab/develop/notes/lfs.md",
    )
    assert ref.ref == "develop"
    assert ref.path == "notes/lfs.md"


def test_parse_rejects_non_github():
    with pytest.raises(GitHubFetchError):
        parse_github_url("https://gitlab.com/acme/lab/blob/main/x.md")


def test_detect_kind_and_companions():
    assert detect_kind("a/b/design.excalidraw.png") == ShowcaseKind.EXCALIDRAW
    assert detect_kind("a/b/design.excalidraw") == ShowcaseKind.EXCALIDRAW
    assert is_excalidraw_embed("design.excalidraw.png")
    assert is_excalidraw_source("design.excalidraw")
    assert not is_excalidraw_source("design.excalidraw.png")
    assert detect_kind("notes/lfs.md") == ShowcaseKind.MARKDOWN
    assert detect_kind("img/arch.png") == ShowcaseKind.IMAGE
    assert companion_preview_paths("design.excalidraw") == ["design.excalidraw.png"]


def test_resolve_excalidraw_ref_prefers_embedded_png():
    ref = parse_github_url(
        "https://github.com/acme/lab/blob/main/designs/api.excalidraw",
    )
    with patch("devresurge.profiles.github.fetch_bytes", return_value=b"PNG"):
        resolved = resolve_excalidraw_ref(ref)
    assert resolved.path == "designs/api.excalidraw.png"


def test_resolve_excalidraw_ref_keeps_png_url():
    ref = parse_github_url(
        "https://github.com/acme/lab/blob/main/designs/api.excalidraw.png",
    )
    with patch("devresurge.profiles.github.fetch_bytes", return_value=b"PNG") as fetch:
        resolved = resolve_excalidraw_ref(ref)
    fetch.assert_called_once()
    assert resolved.path == "designs/api.excalidraw.png"


def test_resolve_excalidraw_ref_rejects_json_without_png():
    ref = parse_github_url(
        "https://github.com/acme/lab/blob/main/designs/api.excalidraw",
    )
    with patch("devresurge.profiles.github.fetch_bytes", side_effect=GitHubFetchError("missing")):
        with pytest.raises(GitHubFetchError, match="excalidraw.png"):
            resolve_excalidraw_ref(ref)


def test_showcase_sync_excalidraw_png():
    profile = ProfileFactory()
    item = ShowcaseItem(
        profile=profile,
        title="URL shortener",
        github_url="https://github.com/acme/lab/blob/main/designs/api.excalidraw.png",
    )
    with patch("devresurge.profiles.github.fetch_bytes", return_value=b"\x89PNG"):
        item.sync_from_github()
    assert item.kind == ShowcaseKind.EXCALIDRAW
    assert item.preview_image_url.endswith("designs/api.excalidraw.png")
    assert item.content_cache == ""
    assert item.content_sha


def test_public_showcase_detail_renders_excalidraw_png(client):
    profile = ProfileFactory(is_public=True, handle="ada")
    item = ShowcaseItemFactory(
        profile=profile,
        title="System design",
        slug="system-design",
        kind=ShowcaseKind.EXCALIDRAW,
        github_path="designs/api.excalidraw.png",
        preview_image_url=(
            "https://raw.githubusercontent.com/acme/lab/main/designs/api.excalidraw.png"
        ),
        content_cache="",
        is_published=True,
    )
    response = client.get(item.get_absolute_url())
    assert response.status_code == 200
    assert b"api.excalidraw.png" in response.content
    assert b"esm.sh" not in response.content
    assert b"dr-excalidraw-mount" not in response.content


def test_showcase_create_syncs_from_github(client):
    user = UserFactory()
    client.force_login(user)
    body = "# Linux from scratch\n\nBuild your own toolchain."

    with patch("devresurge.profiles.github.fetch_text", return_value=body):
        with patch("devresurge.profiles.github.find_preview_url", return_value=""):
            response = client.post(
                reverse("profiles:showcase_create"),
                {
                    "title": "LFS notes",
                    "summary": "My study notes",
                    "kind": ShowcaseKind.MARKDOWN,
                    "github_url": "https://github.com/acme/lab/blob/main/notes/lfs.md",
                    "tags": "linux, notes",
                    "is_featured": "on",
                    "is_published": "on",
                    "sync_now": "on",
                },
            )
    assert response.status_code == 302
    item = ShowcaseItem.objects.get(profile__user=user)
    assert item.slug == "lfs-notes"
    assert item.content_cache.startswith("# Linux")
    assert item.github_owner == "acme"
    assert item.kind == ShowcaseKind.MARKDOWN


def test_public_showcase_detail_renders_markdown(client):
    profile = ProfileFactory(is_public=True, handle="ada")
    item = ShowcaseItemFactory(
        profile=profile,
        title="System design notes",
        slug="system-design-notes",
        kind=ShowcaseKind.MARKDOWN,
        content_cache="## Caching\n\nUse **Redis**.",
        is_published=True,
    )
    response = client.get(item.get_absolute_url())
    assert response.status_code == 200
    assert b"Redis" in response.content
    assert b"lab" in response.content.lower()


def test_unpublished_showcase_hidden_on_profile(client):
    profile = ProfileFactory(is_public=True, handle="ada")
    ShowcaseItemFactory(
        profile=profile,
        title="Secret draft",
        slug="secret-draft",
        is_published=False,
    )
    ShowcaseItemFactory(
        profile=profile,
        title="Public design",
        slug="public-design",
        is_published=True,
        kind=ShowcaseKind.EXCALIDRAW,
    )
    response = client.get(reverse("profiles:public", kwargs={"handle": "ada"}))
    assert response.status_code == 200
    assert b"Public design" in response.content
    assert b"Secret draft" not in response.content

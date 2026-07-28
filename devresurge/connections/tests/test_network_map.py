from __future__ import annotations

from http import HTTPStatus

import pytest
from django.urls import reverse

from devresurge.connections.graph import build_network_graph
from devresurge.connections.models import Connection
from devresurge.connections.models import ConnectionStatus
from devresurge.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def _accept(a, b, *, relation="peer"):
    return Connection.objects.create(
        requester=a,
        addressee=b,
        status=ConnectionStatus.ACCEPTED,
        relation=relation,
    )


def test_network_map_requires_login(client):
    response = client.get(reverse("connections:map"))
    assert response.status_code == HTTPStatus.FOUND
    assert "/accounts/login/" in response.url


def test_owner_map_redirects_to_public_map_when_listed(client):
    me = UserFactory()
    me.profile.is_public = True
    me.profile.save()
    client.force_login(me)
    response = client.get(reverse("connections:map"))
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == reverse(
        "profiles:network_map",
        kwargs={"handle": me.profile.handle},
    )


def test_owner_map_preserves_mutual_query_on_redirect(client):
    me = UserFactory()
    me.profile.is_public = True
    me.profile.save()
    client.force_login(me)
    response = client.get(reverse("connections:map"), {"mutual": "0"})
    assert response.status_code == HTTPStatus.FOUND
    assert "mutual=0" in response.url


def test_private_owner_map_renders_preview(client):
    me = UserFactory()
    peer = UserFactory()
    me.profile.is_public = False
    me.profile.save()
    peer.profile.display_name = "Peer One"
    peer.profile.is_public = True
    peer.profile.save()
    _accept(me, peer, relation="collaborator")
    client.force_login(me)
    response = client.get(reverse("connections:map"))
    assert response.status_code == HTTPStatus.OK
    assert b"Private preview" in response.content
    assert b"dr-network-map" in response.content
    assert b"dr-main--map" in response.content
    assert b"dr-map-stage" in response.content
    assert peer.profile.handle.encode() in response.content
    assert response.context["is_public_map"] is False


def test_network_map_json_payload(client):
    me = UserFactory()
    a = UserFactory()
    b = UserFactory()
    a.profile.is_public = True
    a.profile.save()
    b.profile.is_public = True
    b.profile.save()
    _accept(me, a)
    _accept(me, b)
    _accept(a, b)  # mutual edge among peers
    client.force_login(me)

    response = client.get(reverse("connections:map_data"))
    assert response.status_code == HTTPStatus.OK
    assert response["Cache-Control"] == "private, no-store"
    data = response.json()
    assert data["me_id"] == me.pk
    assert len(data["nodes"]) == 3
    direct = [e for e in data["edges"] if e["kind"] == "direct"]
    mutual = [e for e in data["edges"] if e["kind"] == "mutual"]
    assert len(direct) == 2
    assert len(mutual) == 1
    assert data["stats"]["connections"] == 2
    assert data["stats"]["mutual_edges"] == 1
    assert data["stats"]["private_omitted"] == 0


def test_build_network_graph_omits_private_peers():
    me = UserFactory()
    public = UserFactory()
    private = UserFactory()
    public.profile.is_public = True
    public.profile.save()
    private.profile.is_public = False
    private.profile.save()
    _accept(me, public)
    _accept(me, private)

    graph = build_network_graph(me, public_only=True)
    ids = {n["id"] for n in graph["nodes"]}
    assert me.pk in ids
    assert public.pk in ids
    assert private.pk not in ids
    assert graph["stats"]["connections"] == 1
    assert graph["stats"]["private_omitted"] == 1
    assert all(n["is_public"] or n["is_self"] for n in graph["nodes"])


def test_build_network_graph_can_omit_mutual():
    me = UserFactory()
    a = UserFactory()
    b = UserFactory()
    a.profile.is_public = True
    a.profile.save()
    b.profile.is_public = True
    b.profile.save()
    _accept(me, a)
    _accept(me, b)
    _accept(a, b)
    graph = build_network_graph(me, include_mutual=False)
    assert all(e["kind"] == "direct" for e in graph["edges"])
    assert graph["stats"]["mutual_edges"] == 0


def test_map_data_hides_emails(client):
    me = UserFactory()
    peer = UserFactory()
    peer.profile.is_public = True
    peer.profile.save()
    _accept(me, peer)
    client.force_login(me)
    body = client.get(reverse("connections:map_data")).content.decode()
    assert me.email not in body
    assert peer.email not in body


def test_public_network_map_is_anonymous(client):
    host = UserFactory()
    peer = UserFactory()
    host.profile.is_public = True
    host.profile.save()
    peer.profile.is_public = True
    peer.profile.display_name = "Public Peer"
    peer.profile.save()
    _accept(host, peer)

    url = reverse("profiles:network_map", kwargs={"handle": host.profile.handle})
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert b"dr-network-map" in response.content
    assert b"dr-main--map" in response.content
    assert b"dr-map-canvas-wrap" in response.content
    assert peer.profile.handle.encode() in response.content
    assert response.context["is_public_map"] is True
    assert b"my map" not in response.content
    assert b"public map" not in response.content


def test_public_network_map_404_for_private_profile(client):
    host = UserFactory()
    host.profile.is_public = False
    host.profile.save()
    response = client.get(
        reverse("profiles:network_map", kwargs={"handle": host.profile.handle}),
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_public_network_map_json_excludes_private_peers(client):
    host = UserFactory()
    public = UserFactory()
    private = UserFactory()
    host.profile.is_public = True
    host.profile.save()
    public.profile.is_public = True
    public.profile.save()
    private.profile.is_public = False
    private.profile.save()
    _accept(host, public)
    _accept(host, private)

    response = client.get(
        reverse("profiles:network_map_data", kwargs={"handle": host.profile.handle}),
    )
    assert response.status_code == HTTPStatus.OK
    assert "public" in response["Cache-Control"]
    data = response.json()
    ids = {n["id"] for n in data["nodes"]}
    assert host.pk in ids
    assert public.pk in ids
    assert private.pk not in ids
    assert data["stats"]["private_omitted"] == 1
    body = response.content.decode()
    assert private.email not in body
    assert private.profile.handle not in body


def test_sitemap_includes_public_network_maps(client):
    public = UserFactory()
    private = UserFactory()
    public.profile.is_public = True
    public.profile.save()
    private.profile.is_public = False
    private.profile.save()

    response = client.get(reverse("sitemap"), {"section": "network_maps"})
    assert response.status_code == HTTPStatus.OK
    body = response.content.decode()
    public_map = reverse("profiles:network_map", kwargs={"handle": public.profile.handle})
    private_map = reverse("profiles:network_map", kwargs={"handle": private.profile.handle})
    assert public_map in body
    assert private_map not in body

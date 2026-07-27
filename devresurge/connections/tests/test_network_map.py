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


def test_network_map_renders_for_user(client):
    me = UserFactory()
    peer = UserFactory()
    peer.profile.display_name = "Peer One"
    peer.profile.save()
    _accept(me, peer, relation="collaborator")
    client.force_login(me)
    response = client.get(reverse("connections:map"))
    assert response.status_code == HTTPStatus.OK
    assert b"network map" in response.content
    assert b"dr-network-map" in response.content
    assert peer.profile.handle.encode() in response.content


def test_network_map_json_payload(client):
    me = UserFactory()
    a = UserFactory()
    b = UserFactory()
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


def test_build_network_graph_can_omit_mutual():
    me = UserFactory()
    a = UserFactory()
    b = UserFactory()
    _accept(me, a)
    _accept(me, b)
    _accept(a, b)
    graph = build_network_graph(me, include_mutual=False)
    assert all(e["kind"] == "direct" for e in graph["edges"])
    assert graph["stats"]["mutual_edges"] == 0


def test_map_data_hides_emails(client):
    me = UserFactory()
    peer = UserFactory()
    _accept(me, peer)
    client.force_login(me)
    body = client.get(reverse("connections:map_data")).content.decode()
    assert me.email not in body
    assert peer.email not in body

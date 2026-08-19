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
    assert "open_to_work" in data["stats"]
    peer_nodes = [n for n in data["nodes"] if not n["is_self"]]
    assert all("intents" in n for n in peer_nodes)


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


def test_build_network_graph_exposes_open_to_intents():
    me = UserFactory()
    peer = UserFactory()
    peer.profile.is_public = True
    peer.profile.available_for_hire = True
    peer.profile.open_to_collaborate = True
    peer.profile.save()
    _accept(me, peer)

    graph = build_network_graph(me, public_only=True)
    node = next(n for n in graph["nodes"] if n["id"] == peer.pk)
    assert node["open_to_work"] is True
    assert node["open_to_collaborate"] is True
    assert "hire" in node["intents"]
    assert "collaborate" in node["intents"]
    assert graph["stats"]["open_to_work"] == 1
    assert graph["stats"]["open_to_collaborate"] == 1


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
    assert b"linkedin.com/sharing" in response.content
    assert b"data-map-intent" in response.content
    assert peer.profile.handle.encode() in response.content
    assert response.context["is_public_map"] is True
    assert response.context["map_share"] is not None
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
    host_node = next(n for n in data["nodes"] if n["id"] == host.pk)
    assert host_node["is_center"] is True
    assert host_node["is_self"] is False
    body = response.content.decode()
    assert private.email not in body
    assert private.profile.handle not in body


def test_public_network_map_marks_you_only_for_owner(client):
    host = UserFactory()
    guest = UserFactory()
    host.profile.is_public = True
    host.profile.save()
    guest.profile.is_public = True
    guest.profile.save()
    _accept(host, guest)

    anon = client.get(
        reverse("profiles:network_map_data", kwargs={"handle": host.profile.handle}),
    ).json()
    host_anon = next(n for n in anon["nodes"] if n["id"] == host.pk)
    assert host_anon["is_self"] is False
    assert host_anon["is_center"] is True

    client.force_login(guest)
    as_guest = client.get(
        reverse("profiles:network_map_data", kwargs={"handle": host.profile.handle}),
    ).json()
    host_guest = next(n for n in as_guest["nodes"] if n["id"] == host.pk)
    assert host_guest["is_self"] is False

    client.force_login(host)
    as_owner = client.get(
        reverse("profiles:network_map_data", kwargs={"handle": host.profile.handle}),
    ).json()
    host_owner = next(n for n in as_owner["nodes"] if n["id"] == host.pk)
    assert host_owner["is_self"] is True
    assert host_owner["is_center"] is True

    page = client.get(
        reverse("profiles:network_map", kwargs={"handle": host.profile.handle}),
    )
    assert page.status_code == HTTPStatus.OK
    # HUD uses handle for public maps, not the generic "you" label for guests.
    client.logout()
    anon_page = client.get(
        reverse("profiles:network_map", kwargs={"handle": host.profile.handle}),
    )
    assert anon_page.status_code == HTTPStatus.OK
    embedded = anon_page.context["graph"]
    center = next(n for n in embedded["nodes"] if n["is_center"])
    assert center["id"] == host.pk
    assert center["is_self"] is False
    assert all(not n["is_self"] for n in embedded["nodes"])
    assert b"· you" not in anon_page.content
    assert host.profile.handle.encode() in anon_page.content


def test_explore_map_is_anonymous(client):
    a = UserFactory()
    b = UserFactory()
    a.profile.is_public = True
    a.profile.save()
    b.profile.is_public = True
    b.profile.available_for_hire = True
    b.profile.save()
    _accept(a, b)

    response = client.get(reverse("profiles:explore_map"))
    assert response.status_code == HTTPStatus.OK
    assert response.context["is_explore_map"] is True
    assert b"dr-network-map" in response.content
    assert b"explore the network" in response.content
    assert b"Want a node on this map?" in response.content
    assert a.profile.handle.encode() in response.content
    assert b.profile.handle.encode() in response.content


def test_explore_map_json_public_only(client):
    public_a = UserFactory()
    public_b = UserFactory()
    private = UserFactory()
    public_a.profile.is_public = True
    public_a.profile.save()
    public_b.profile.is_public = True
    public_b.profile.save()
    private.profile.is_public = False
    private.profile.save()
    _accept(public_a, public_b)
    _accept(public_a, private)

    response = client.get(reverse("profiles:explore_map_data"))
    assert response.status_code == HTTPStatus.OK
    assert response["Cache-Control"].startswith("public")
    data = response.json()
    ids = {n["id"] for n in data["nodes"]}
    assert public_a.pk in ids
    assert public_b.pk in ids
    assert private.pk not in ids
    assert data["me_id"] is None
    assert data["stats"]["people"] == 2


def test_build_explore_graph_caps_and_stats():
    from devresurge.connections.graph import build_explore_graph

    host = UserFactory()
    host.profile.is_public = True
    host.profile.save()
    peers = []
    for _ in range(3):
        peer = UserFactory()
        peer.profile.is_public = True
        peer.profile.available_for_hire = True
        peer.profile.save()
        peers.append(peer)
        _accept(host, peer)

    graph = build_explore_graph(limit=10)
    assert graph["stats"]["people"] >= 4
    assert graph["stats"]["open_to_work"] >= 3
    assert graph["stats"]["links"] >= 3
    assert all(not n["is_self"] for n in graph["nodes"])


def test_public_network_map_invite_share_and_landing(client):
    host = UserFactory()
    guest = UserFactory()
    host.profile.is_public = True
    host.profile.save()
    guest.profile.is_public = True
    guest.profile.save()

    url = reverse("profiles:network_map", kwargs={"handle": host.profile.handle})
    anon = client.get(url)
    assert anon.status_code == HTTPStatus.OK
    assert anon.context["map_invite"] is None
    assert anon.context["is_map_owner"] is False
    assert b"invite to connect" not in anon.content

    landing = client.get(url, {"invite": "1"})
    assert landing.status_code == HTTPStatus.OK
    assert landing.context["invite_landing"] is True
    assert landing.context["map_invite"] is None
    assert b"invited you to connect" in landing.content
    assert b"join &amp; connect" in landing.content or b"login to connect" in landing.content
    assert b"invite to connect" not in landing.content

    client.force_login(guest)
    guest_page = client.get(url)
    assert guest_page.context["map_invite"] is None
    assert guest_page.context["is_map_owner"] is False
    assert b"invite to connect" not in guest_page.content

    guest_landing = client.get(url, {"invite": "1"})
    assert guest_landing.context["invite_landing"] is True
    assert guest_landing.context["can_connect"] is True
    assert guest_landing.context["map_invite"] is None
    assert b"Send connection request" in guest_landing.content or b"Connect" in guest_landing.content
    assert b"invite to connect" not in guest_landing.content

    client.force_login(host)
    owner = client.get(url, {"invite": "1"})
    assert owner.context["invite_landing"] is False
    assert owner.context["is_map_owner"] is True
    assert owner.context["map_invite"] is not None
    assert "invite=1" in owner.context["map_invite"]["page_url"]
    assert "wa.me" in owner.context["map_invite"]["whatsapp"]
    assert b"invite to connect" in owner.content
    assert b"copy invite" in owner.content


def test_build_map_invite_share_links():
    from devresurge.connections.share import build_map_invite_share_links

    links = build_map_invite_share_links(
        page_url="https://example.com/u/ada/map/?invite=1",
        handle="ada",
        name="Ada",
    )
    assert "invite=1" in links["page_url"]
    assert "linkedin.com/sharing" in links["linkedin"]
    assert "twitter.com/intent/tweet" in links["x"]
    assert "wa.me" in links["whatsapp"]
    assert links["email"].startswith("mailto:")
    assert "Connect with Ada" in links["caption"] or "Connect with" in links["caption"]


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

    static = client.get(reverse("sitemap"), {"section": "static"})
    assert static.status_code == HTTPStatus.OK
    assert reverse("profiles:explore_map") in static.content.decode()

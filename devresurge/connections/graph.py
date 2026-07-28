"""Build privacy-safe graph payloads for the interactive network map."""

from __future__ import annotations

from typing import Any

from django.db.models import Q

from .models import Connection
from .models import ConnectionStatus


def _profile_is_public(user) -> bool:
    profile = getattr(user, "profile", None)
    return bool(profile is not None and profile.is_public)


def _node_from_user(user, *, is_self: bool = False) -> dict[str, Any]:
    profile = getattr(user, "profile", None)
    handle = getattr(profile, "handle", "") or ""
    avatar = ""
    if profile is not None and profile.avatar:
        try:
            avatar = profile.avatar.url
        except ValueError:
            avatar = ""
    is_public = bool(getattr(profile, "is_public", False))
    open_to_work = bool(getattr(profile, "available_for_hire", False))
    open_to_collaborate = bool(getattr(profile, "open_to_collaborate", False))
    open_to_mentor = bool(getattr(profile, "open_to_mentor", False))
    open_to_learning = bool(getattr(profile, "open_to_learning", False))
    intents: list[str] = []
    if open_to_work:
        intents.append("hire")
    if open_to_collaborate:
        intents.append("collaborate")
    if open_to_mentor:
        intents.append("mentor")
    if open_to_learning:
        intents.append("learning")
    return {
        "id": user.pk,
        "handle": handle,
        "name": profile.public_name if profile is not None else str(user.pk),
        "initials": profile.initials if profile is not None else "?",
        "role": profile.get_primary_role_display() if profile is not None else "",
        "location": (profile.location or "") if profile is not None else "",
        "avatar": avatar,
        # Only link out to public profiles (self always may deep-link when public).
        "url": (
            profile.get_absolute_url()
            if profile is not None and handle and (is_self or is_public)
            else ""
        ),
        "open_to_work": open_to_work,
        "open_to_collaborate": open_to_collaborate,
        "open_to_mentor": open_to_mentor,
        "open_to_learning": open_to_learning,
        "intents": intents,
        "is_self": is_self,
        "is_public": is_public,
    }


def build_network_graph(
    user,
    *,
    include_mutual: bool = True,
    public_only: bool = True,
) -> dict[str, Any]:
    """Return ego network for ``user``.

    Nodes: the viewer + accepted 1st-degree connections.
    When ``public_only`` (default), private accounts are omitted from nodes and
    edges — required for any map that can be shared or embedded publicly.

    Edges: viewer↔peer (with relation), and optionally peer↔peer when two of
    the viewer's connections are also connected to each other.
    """
    accepted = list(
        Connection.objects.involving(user)
        .filter(status=ConnectionStatus.ACCEPTED)
        .select_related("requester__profile", "addressee__profile"),
    )

    me = _node_from_user(user, is_self=True)
    nodes_by_id: dict[int, dict[str, Any]] = {user.pk: me}
    edges: list[dict[str, Any]] = []
    peer_ids: list[int] = []
    private_omitted = 0

    for conn in accepted:
        other = conn.other_user(user)
        if public_only and not _profile_is_public(other):
            private_omitted += 1
            continue
        if other.pk not in nodes_by_id:
            nodes_by_id[other.pk] = _node_from_user(other)
            peer_ids.append(other.pk)
        edges.append(
            {
                "source": user.pk,
                "target": other.pk,
                "relation": conn.relation,
                "label": conn.get_relation_display(),
                "kind": "direct",
            },
        )

    mutual_count = 0
    if include_mutual and len(peer_ids) >= 2:
        # Edges among peers that share an accepted connection (public set only).
        peer_links = (
            Connection.objects.filter(status=ConnectionStatus.ACCEPTED)
            .filter(
                Q(requester_id__in=peer_ids, addressee_id__in=peer_ids),
            )
            .select_related("requester__profile", "addressee__profile")
        )
        seen_pairs: set[tuple[int, int]] = set()
        for conn in peer_links:
            a, b = conn.requester_id, conn.addressee_id
            if a == b:
                continue
            pair = (min(a, b), max(a, b))
            if pair in seen_pairs:
                continue
            seen_pairs.add(pair)
            edges.append(
                {
                    "source": a,
                    "target": b,
                    "relation": conn.relation,
                    "label": conn.get_relation_display(),
                    "kind": "mutual",
                },
            )
            mutual_count += 1

    # Relation histogram for filters / legend.
    relation_counts: dict[str, int] = {}
    for edge in edges:
        if edge["kind"] != "direct":
            continue
        relation_counts[edge["relation"]] = relation_counts.get(edge["relation"], 0) + 1

    peers = [nodes_by_id[pid] for pid in peer_ids]
    open_to_work = sum(1 for n in peers if n["open_to_work"])
    open_to_collaborate = sum(1 for n in peers if n["open_to_collaborate"])
    open_to_mentor = sum(1 for n in peers if n["open_to_mentor"])
    open_to_learning = sum(1 for n in peers if n["open_to_learning"])

    return {
        "me_id": user.pk,
        "nodes": list(nodes_by_id.values()),
        "edges": edges,
        "stats": {
            "connections": len(peer_ids),
            "mutual_edges": mutual_count,
            "relations": relation_counts,
            "private_omitted": private_omitted,
            "open_to_work": open_to_work,
            "open_to_collaborate": open_to_collaborate,
            "open_to_mentor": open_to_mentor,
            "open_to_learning": open_to_learning,
        },
    }


def build_explore_graph(*, limit: int = 120) -> dict[str, Any]:
    """Public community graph for anonymous exploration.

    Only publicly listed accounts and edges between them. Capped by degree so
    the canvas stays usable while still showcasing real network signal.
    """
    limit = max(8, min(int(limit or 120), 200))
    public_links = list(
        Connection.objects.filter(status=ConnectionStatus.ACCEPTED)
        .filter(
            requester__profile__is_public=True,
            addressee__profile__is_public=True,
        )
        .select_related("requester__profile", "addressee__profile")
        .order_by("-created_at")[:800],
    )

    degree: dict[int, int] = {}
    for conn in public_links:
        degree[conn.requester_id] = degree.get(conn.requester_id, 0) + 1
        degree[conn.addressee_id] = degree.get(conn.addressee_id, 0) + 1

    ranked_ids = sorted(degree.keys(), key=lambda uid: (-degree[uid], uid))[:limit]
    keep = set(ranked_ids)

    nodes_by_id: dict[int, dict[str, Any]] = {}
    for conn in public_links:
        for user in (conn.requester, conn.addressee):
            if user.pk in keep and user.pk not in nodes_by_id:
                nodes_by_id[user.pk] = _node_from_user(user)

    edges: list[dict[str, Any]] = []
    seen_pairs: set[tuple[int, int]] = set()
    relation_counts: dict[str, int] = {}
    for conn in public_links:
        a, b = conn.requester_id, conn.addressee_id
        if a not in keep or b not in keep or a == b:
            continue
        pair = (min(a, b), max(a, b))
        if pair in seen_pairs:
            continue
        seen_pairs.add(pair)
        edges.append(
            {
                "source": a,
                "target": b,
                "relation": conn.relation,
                "label": conn.get_relation_display(),
                "kind": "direct",
            },
        )
        relation_counts[conn.relation] = relation_counts.get(conn.relation, 0) + 1

    nodes = list(nodes_by_id.values())
    open_to_work = sum(1 for n in nodes if n["open_to_work"])
    open_to_collaborate = sum(1 for n in nodes if n["open_to_collaborate"])
    open_to_mentor = sum(1 for n in nodes if n["open_to_mentor"])
    open_to_learning = sum(1 for n in nodes if n["open_to_learning"])

    return {
        "me_id": None,
        "nodes": nodes,
        "edges": edges,
        "stats": {
            "connections": len(nodes),
            "people": len(nodes),
            "links": len(edges),
            "mutual_edges": 0,
            "relations": relation_counts,
            "private_omitted": 0,
            "open_to_work": open_to_work,
            "open_to_collaborate": open_to_collaborate,
            "open_to_mentor": open_to_mentor,
            "open_to_learning": open_to_learning,
            "capped": len(degree) > len(nodes),
            "total_public_linked": len(degree),
        },
    }

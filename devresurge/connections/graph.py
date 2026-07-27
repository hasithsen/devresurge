"""Build privacy-safe graph payloads for the interactive network map."""

from __future__ import annotations

from typing import Any

from django.db.models import Q

from .models import Connection
from .models import ConnectionStatus


def _node_from_user(user, *, is_self: bool = False) -> dict[str, Any]:
    profile = getattr(user, "profile", None)
    handle = getattr(profile, "handle", "") or ""
    avatar = ""
    if profile is not None and profile.avatar:
        try:
            avatar = profile.avatar.url
        except ValueError:
            avatar = ""
    return {
        "id": user.pk,
        "handle": handle,
        "name": profile.public_name if profile is not None else str(user.pk),
        "initials": profile.initials if profile is not None else "?",
        "role": profile.get_primary_role_display() if profile is not None else "",
        "location": (profile.location or "") if profile is not None else "",
        "avatar": avatar,
        "url": (
            profile.get_absolute_url()
            if profile is not None and handle and (is_self or profile.is_public)
            else ""
        ),
        "open_to_work": bool(getattr(profile, "available_for_hire", False)),
        "is_self": is_self,
        "is_public": bool(getattr(profile, "is_public", False)),
    }


def build_network_graph(user, *, include_mutual: bool = True) -> dict[str, Any]:
    """Return ego network for ``user``.

    Nodes: the viewer + every accepted 1st-degree connection.
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

    for conn in accepted:
        other = conn.other_user(user)
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
        # Edges among peers that share an accepted connection.
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

    return {
        "me_id": user.pk,
        "nodes": list(nodes_by_id.values()),
        "edges": edges,
        "stats": {
            "connections": len(peer_ids),
            "mutual_edges": mutual_count,
            "relations": relation_counts,
        },
    }

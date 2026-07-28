"""Social share links for public network maps."""

from __future__ import annotations

from urllib.parse import urlencode


def build_map_share_links(*, page_url: str, handle: str) -> dict[str, str]:
    """Return share URLs for a public ``/u/<handle>/map/`` page.

    Complements LinkedIn: career network stays there; this map is shareable
    technical-network proof (public connections, relations, open-to intents).
    """
    handle = (handle or "").lstrip("@")
    caption = (
        f"@{handle}’s public connection map on DevResurge — "
        "see peers, mutuals, and open-to intents. "
        "LinkedIn for the career network; DevResurge for the signal."
    )
    caption = " ".join(caption.split())
    if len(caption) > 240:
        caption = caption[:237].rstrip() + "…"

    return {
        "linkedin": (
            "https://www.linkedin.com/sharing/share-offsite/?"
            + urlencode({"url": page_url})
        ),
        "x": (
            "https://twitter.com/intent/tweet?"
            + urlencode({"text": caption, "url": page_url})
        ),
        "reddit": (
            "https://www.reddit.com/submit?"
            + urlencode({"url": page_url, "title": caption})
        ),
        "email": "mailto:?"
        + urlencode(
            {
                "subject": f"@{handle} network map · DevResurge",
                "body": f"{caption}\n\n{page_url}",
            },
        ),
        "caption": caption,
        "page_url": page_url,
    }


def build_explore_share_links(*, page_url: str) -> dict[str, str]:
    """Share URLs for the public community explore map at ``/map/``."""
    caption = (
        "Explore the public DevResurge network map — developers open to work, "
        "collaborate, and mentor. Technical signal that complements LinkedIn."
    )
    caption = " ".join(caption.split())
    if len(caption) > 240:
        caption = caption[:237].rstrip() + "…"

    return {
        "linkedin": (
            "https://www.linkedin.com/sharing/share-offsite/?"
            + urlencode({"url": page_url})
        ),
        "x": (
            "https://twitter.com/intent/tweet?"
            + urlencode({"text": caption, "url": page_url})
        ),
        "reddit": (
            "https://www.reddit.com/submit?"
            + urlencode({"url": page_url, "title": caption})
        ),
        "email": "mailto:?"
        + urlencode(
            {
                "subject": "DevResurge network map",
                "body": f"{caption}\n\n{page_url}",
            },
        ),
        "caption": caption,
        "page_url": page_url,
    }


def build_map_invite_share_links(
    *,
    page_url: str,
    handle: str,
    name: str = "",
) -> dict[str, str]:
    """Share URLs that invite someone to connect via a public map.

    ``page_url`` should already include ``?invite=1`` so recipients land on the
    map with a connect CTA. Share-friendly copy works on LinkedIn, X, Reddit,
    WhatsApp, and email.
    """
    handle = (handle or "").lstrip("@")
    who = (name or "").strip() or f"@{handle}"
    caption = (
        f"Connect with {who} on DevResurge — explore @{handle}’s public "
        "network map (peers, mutuals, open-to intents). "
        "Technical signal that complements LinkedIn."
    )
    caption = " ".join(caption.split())
    if len(caption) > 240:
        caption = caption[:237].rstrip() + "…"

    return {
        "linkedin": (
            "https://www.linkedin.com/sharing/share-offsite/?"
            + urlencode({"url": page_url})
        ),
        "x": (
            "https://twitter.com/intent/tweet?"
            + urlencode({"text": caption, "url": page_url})
        ),
        "reddit": (
            "https://www.reddit.com/submit?"
            + urlencode({"url": page_url, "title": caption})
        ),
        "whatsapp": "https://wa.me/?" + urlencode({"text": f"{caption}\n{page_url}"}),
        "email": "mailto:?"
        + urlencode(
            {
                "subject": f"Connect with @{handle} on DevResurge",
                "body": f"{caption}\n\n{page_url}",
            },
        ),
        "caption": caption,
        "page_url": page_url,
        "handle": handle,
    }

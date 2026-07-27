"""Build absolute social share links for badges."""

from __future__ import annotations

from urllib.parse import urlencode


def build_badge_share_links(
    *,
    page_url: str,
    title: str,
    description: str,
    earned: bool = False,
) -> dict[str, str]:
    """Return platform share URLs for a badge page.

    LinkedIn only accepts a URL; X/Reddit/email carry a short caption.
    """
    if earned:
        caption = f"I earned “{title}” on DevResurge — {description}"
    else:
        caption = f"{title} — {description} · DevResurge"

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
                "subject": f"{title} · DevResurge",
                "body": f"{caption}\n\n{page_url}",
            },
        ),
        "caption": caption,
        "page_url": page_url,
    }

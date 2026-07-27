"""Embeddable SVG for achievement badges."""

from __future__ import annotations

import html
import re

_XML_SAFE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def _xml_text(value: str, *, limit: int = 80) -> str:
    cleaned = _XML_SAFE.sub("", (value or "").strip())[:limit]
    return html.escape(cleaned, quote=False)


def render_achievement_badge_svg(
    badge,
    *,
    holder_handle: str | None = None,
    width: int = 280,
    height: int = 72,
) -> str:
    """Return a compact SVG chip for READMEs / profile embeds."""
    title = _xml_text(badge.title, limit=28)
    icon = _xml_text(badge.icon or "★", limit=4)
    category = _xml_text(badge.get_category_display(), limit=20)
    holder = _xml_text(f"@{holder_handle}", limit=24) if holder_handle else ""

    holder_svg = ""
    if holder:
        holder_svg = (
            f'<text x="56" y="58" fill="#7cf0a8" font-size="11" '
            f'font-family="ui-monospace, SFMono-Regular, Menlo, monospace">'
            f"{holder}</text>"
        )
        desc_y = 42
    else:
        desc_y = 50

    desc = _xml_text(badge.description, limit=42)
    aria = f"{title} badge on DevResurge"
    if holder_handle:
        aria = f"{title} earned by @{holder_handle} on DevResurge"

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" role="img" aria-label="{aria}">
  <title>{title} — DevResurge</title>
  <rect width="100%" height="100%" rx="10" fill="#0b0f0d" stroke="#1f2c30"/>
  <rect x="0" y="0" width="6" height="100%" fill="#7cf0a8"/>
  <circle cx="34" cy="36" r="16" fill="#14201a" stroke="#2a3f36"/>
  <text x="34" y="41" text-anchor="middle" fill="#7cf0a8" font-size="14"
        font-family="ui-monospace, SFMono-Regular, Menlo, monospace">{icon}</text>
  <text x="56" y="28" fill="#d8e8df" font-size="14" font-weight="700"
        font-family="ui-monospace, SFMono-Regular, Menlo, monospace">{title}</text>
  <text x="56" y="{desc_y}" fill="#7a8a85" font-size="11"
        font-family="ui-monospace, SFMono-Regular, Menlo, monospace">{desc if not holder else category}</text>
  {holder_svg}
</svg>
"""

"""Embeddable SVG for achievement badges."""

from __future__ import annotations

import html
import re

_XML_SAFE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")

# Approximate advance width for ui-monospace / SFMono at a given font size.
_MONO_ADVANCE = 0.62
_MIN_WIDTH = 260
_MAX_WIDTH = 520
_PAD_LEFT = 56  # icon column + text start
_PAD_RIGHT = 18


def _xml_escape(value: str) -> str:
    return html.escape(_XML_SAFE.sub("", (value or "").strip()), quote=False)


def _text_width(text: str, font_size: float) -> float:
    return len(text) * font_size * _MONO_ADVANCE


def _fit_text(raw: str, *, max_width: float, font_size: float) -> str:
    """Escape and ellipsize so the glyph string fits ``max_width`` px."""
    cleaned = _XML_SAFE.sub("", (raw or "").strip())
    if not cleaned or _text_width(cleaned, font_size) <= max_width:
        return html.escape(cleaned, quote=False)
    ellipsis = "…"
    budget = max_width - _text_width(ellipsis, font_size)
    if budget <= 0:
        return ellipsis
    lo, hi = 0, len(cleaned)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if _text_width(cleaned[:mid], font_size) <= budget:
            lo = mid
        else:
            hi = mid - 1
    cut = cleaned[:lo].rstrip()
    if " " in cut and len(cut) > 8:
        cut = cut.rsplit(" ", 1)[0]
    return html.escape(f"{cut}{ellipsis}", quote=False)


def render_achievement_badge_svg(
    badge,
    *,
    holder_handle: str | None = None,
    height: int = 72,
) -> str:
    """Return a compact SVG chip sized to fit title + subtitle without clipping."""
    icon = _xml_escape(badge.icon or "★")[:4]
    title_raw = (badge.title or "").strip()
    category_raw = badge.get_category_display()
    desc_raw = (badge.description or "").strip()
    holder_raw = f"@{holder_handle}" if holder_handle else ""

    # First pass: measure natural widths, then clamp SVG + refit text.
    subtitle_raw = category_raw if holder_handle else desc_raw
    natural = max(
        _text_width(title_raw, 14),
        _text_width(subtitle_raw, 11),
        _text_width(holder_raw, 11) if holder_handle else 0,
        140,
    )
    width = int(min(_MAX_WIDTH, max(_MIN_WIDTH, _PAD_LEFT + natural + _PAD_RIGHT)))
    text_max = width - _PAD_LEFT - _PAD_RIGHT

    title = _fit_text(title_raw, max_width=text_max, font_size=14)
    if holder_handle:
        subtitle = _fit_text(category_raw, max_width=text_max, font_size=11)
        holder = _fit_text(holder_raw, max_width=text_max, font_size=11)
        mid_y, bottom_y = 42, 58
        third_line = (
            f'<text x="{_PAD_LEFT}" y="{bottom_y}" fill="#7cf0a8" font-size="11" '
            f'font-family="ui-monospace, SFMono-Regular, Menlo, monospace">'
            f"{holder}</text>"
        )
    else:
        subtitle = _fit_text(desc_raw, max_width=text_max, font_size=11)
        third_line = ""
        mid_y = 50

    aria_title = _xml_escape(title_raw) or "Badge"
    if holder_handle:
        aria = f"{aria_title} earned by @{_xml_escape(holder_handle)} on DevResurge"
    else:
        aria = f"{aria_title} badge on DevResurge"

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{aria}">
  <title>{aria_title} — DevResurge</title>
  <rect width="100%" height="100%" rx="10" fill="#0b0f0d" stroke="#1f2c30"/>
  <rect x="0" y="0" width="6" height="100%" fill="#7cf0a8"/>
  <circle cx="34" cy="36" r="16" fill="#14201a" stroke="#2a3f36"/>
  <text x="34" y="41" text-anchor="middle" fill="#7cf0a8" font-size="14"
        font-family="ui-monospace, SFMono-Regular, Menlo, monospace">{icon}</text>
  <text x="{_PAD_LEFT}" y="28" fill="#d8e8df" font-size="14" font-weight="700"
        font-family="ui-monospace, SFMono-Regular, Menlo, monospace">{title}</text>
  <text x="{_PAD_LEFT}" y="{mid_y}" fill="#7a8a85" font-size="11"
        font-family="ui-monospace, SFMono-Regular, Menlo, monospace">{subtitle}</text>
  {third_line}
</svg>
"""

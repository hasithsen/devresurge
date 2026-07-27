"""Embeddable SVG for achievement badges."""

from __future__ import annotations

from devresurge.svg_text import fit_canvas_width
from devresurge.svg_text import fit_single_line
from devresurge.svg_text import text_width
from devresurge.svg_text import tspan_lines
from devresurge.svg_text import wrap_words
from devresurge.svg_text import xml_escape

_MIN_WIDTH = 300
_MAX_WIDTH = 580
_PAD_LEFT = 56
_PAD_RIGHT = 20
_LINE_H = 15
# Wide enough that every seeded badge description fits on ≤2 lines with no ellipsis.
_CONTENT_COL = 360


def render_achievement_badge_svg(
    badge,
    *,
    holder_handle: str | None = None,
) -> str:
    """Return an SVG chip sized so title + description never clip."""
    icon = xml_escape(badge.icon or "★")[:4]
    title_raw = (badge.title or "").strip()
    category_raw = badge.get_category_display()
    desc_raw = (badge.description or "").strip()
    holder_raw = f"@{holder_handle}" if holder_handle else ""

    width = fit_canvas_width(
        text_width(title_raw, 14),
        _CONTENT_COL,
        text_width(holder_raw, 11) if holder_handle else 0,
        pad_left=_PAD_LEFT,
        pad_right=_PAD_RIGHT,
        min_width=_MIN_WIDTH,
        max_width=_MAX_WIDTH,
    )
    text_max = width - _PAD_LEFT - _PAD_RIGHT

    title = fit_single_line(title_raw, max_width=text_max, font_size=14)
    # Grow width further if title still needed ellipsis at current size (extreme titles).
    if "…" in title and text_width(title_raw, 14) + _PAD_LEFT + _PAD_RIGHT + 14 <= _MAX_WIDTH:
        width = fit_canvas_width(
            text_width(title_raw, 14),
            _CONTENT_COL,
            pad_left=_PAD_LEFT,
            pad_right=_PAD_RIGHT,
            min_width=_MIN_WIDTH,
            max_width=_MAX_WIDTH,
        )
        text_max = width - _PAD_LEFT - _PAD_RIGHT
        title = fit_single_line(title_raw, max_width=text_max, font_size=14)

    if holder_handle:
        body_lines = wrap_words(category_raw, max_width=text_max, font_size=11, max_lines=1)
        holder_lines = wrap_words(holder_raw, max_width=text_max, font_size=11, max_lines=1)
        body_block = tspan_lines(
            body_lines or [category_raw],
            x=_PAD_LEFT,
            start_y=44,
            line_height=_LINE_H,
            fill="#7a8a85",
            font_size=11,
        )
        holder_block = tspan_lines(
            holder_lines or [holder_raw],
            x=_PAD_LEFT,
            start_y=44 + _LINE_H,
            line_height=_LINE_H,
            fill="#7cf0a8",
            font_size=11,
        )
        extra = f"  {body_block}\n  {holder_block}"
        height = 76
    else:
        body_lines = wrap_words(desc_raw, max_width=text_max, font_size=11, max_lines=2)
        body_block = tspan_lines(
            body_lines,
            x=_PAD_LEFT,
            start_y=46,
            line_height=_LINE_H,
            fill="#7a8a85",
            font_size=11,
        )
        extra = f"  {body_block}"
        height = 72 if len(body_lines) <= 1 else 90

    aria_title = xml_escape(title_raw) or "Badge"
    if holder_handle:
        aria = f"{aria_title} earned by @{xml_escape(holder_handle)} on DevResurge"
    else:
        aria = f"{aria_title} badge on DevResurge"

    icon_cy = height / 2
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{aria}">
  <title>{aria_title} — DevResurge</title>
  <rect width="100%" height="100%" rx="10" fill="#0b0f0d" stroke="#1f2c30"/>
  <rect x="0" y="0" width="6" height="100%" fill="#7cf0a8"/>
  <circle cx="34" cy="{icon_cy}" r="16" fill="#14201a" stroke="#2a3f36"/>
  <text x="34" y="{icon_cy + 5}" text-anchor="middle" fill="#7cf0a8" font-size="14"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">{icon}</text>
  <text x="{_PAD_LEFT}" y="28" fill="#d8e8df" font-size="14" font-weight="700"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">{title}</text>
{extra}
</svg>
"""

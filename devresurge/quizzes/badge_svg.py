"""Embeddable SVG for achievement badges."""

from __future__ import annotations

from devresurge.svg_text import fit_canvas_width
from devresurge.svg_text import fit_single_line
from devresurge.svg_text import text_width
from devresurge.svg_text import tspan_lines
from devresurge.svg_text import wrap_words
from devresurge.svg_text import xml_escape

_MIN_WIDTH = 320
_MAX_WIDTH = 720
_PAD_LEFT = 56
_PAD_RIGHT = 22
_LINE_H = 16
_TITLE_SIZE = 14
_BODY_SIZE = 11


def render_achievement_badge_svg(
    badge,
    *,
    holder_handle: str | None = None,
) -> str:
    """Return an SVG chip sized so title + full description never clip."""
    icon = xml_escape(badge.icon or "★")[:4]
    title_raw = (badge.title or "").strip()
    category_raw = badge.get_category_display()
    desc_raw = (badge.description or "").strip()
    holder_raw = f"@{holder_handle}" if holder_handle else ""

    # Prefer a single-line description: drive canvas width from the full copy.
    body_raw = category_raw if holder_handle else desc_raw
    width = fit_canvas_width(
        text_width(title_raw, _TITLE_SIZE),
        text_width(body_raw, _BODY_SIZE),
        text_width(holder_raw, _BODY_SIZE) if holder_handle else 0,
        pad_left=_PAD_LEFT,
        pad_right=_PAD_RIGHT,
        min_width=_MIN_WIDTH,
        max_width=_MAX_WIDTH,
    )
    text_max = width - _PAD_LEFT - _PAD_RIGHT

    title = fit_single_line(title_raw, max_width=text_max, font_size=_TITLE_SIZE)

    if holder_handle:
        body_lines = wrap_words(
            category_raw,
            max_width=text_max,
            font_size=_BODY_SIZE,
            max_lines=None,
        )
        holder_lines = wrap_words(
            holder_raw,
            max_width=text_max,
            font_size=_BODY_SIZE,
            max_lines=None,
        )
        y = 46
        blocks = [
            tspan_lines(
                body_lines or [category_raw],
                x=_PAD_LEFT,
                start_y=y,
                line_height=_LINE_H,
                fill="#7a8a85",
                font_size=_BODY_SIZE,
            ),
        ]
        y += max(len(body_lines), 1) * _LINE_H
        blocks.append(
            tspan_lines(
                holder_lines or [holder_raw],
                x=_PAD_LEFT,
                start_y=y,
                line_height=_LINE_H,
                fill="#7cf0a8",
                font_size=_BODY_SIZE,
            ),
        )
        extra = "\n".join(f"  {b}" for b in blocks)
        last_y = y + (max(len(holder_lines), 1) - 1) * _LINE_H
        height = max(76, int(last_y + 18))
    else:
        # Unlimited wrap — never ellipsize catalog descriptions.
        body_lines = wrap_words(
            desc_raw,
            max_width=text_max,
            font_size=_BODY_SIZE,
            max_lines=None,
        ) or [desc_raw]
        body_block = tspan_lines(
            body_lines,
            x=_PAD_LEFT,
            start_y=46,
            line_height=_LINE_H,
            fill="#7a8a85",
            font_size=_BODY_SIZE,
        )
        extra = f"  {body_block}"
        last_y = 46 + (len(body_lines) - 1) * _LINE_H
        height = max(72, int(last_y + 18))

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
  <text x="{_PAD_LEFT}" y="28" fill="#d8e8df" font-size="{_TITLE_SIZE}" font-weight="700"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">{title}</text>
{extra}
</svg>
"""

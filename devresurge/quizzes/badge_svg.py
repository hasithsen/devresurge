"""Embeddable SVG for achievement badges."""

from __future__ import annotations

from devresurge.svg_text import tspan_lines
from devresurge.svg_text import wrap_words
from devresurge.svg_text import xml_escape

# Cap width so badges fit inside panels/mobile without horizontal clipping.
_MAX_WIDTH = 380
_PAD_LEFT = 56
_PAD_RIGHT = 18
_LINE_H = 17
_TITLE_SIZE = 14
_BODY_SIZE = 12
# Pixel budget for text — must stay inside the canvas (never overflow).
_CONTENT_W = _MAX_WIDTH - _PAD_LEFT - _PAD_RIGHT
_BODY_MAX_PX = _CONTENT_W - 8
_TITLE_MAX_PX = _CONTENT_W - 8
_TITLE_LINE_H = 18

# Earned (shareable) palette.
_EARNED = {
    "bg": "#0b0f0d",
    "stroke": "#1f2c30",
    "accent": "#7cf0a8",
    "icon_bg": "#14201a",
    "icon_stroke": "#2a3f36",
    "icon": "#7cf0a8",
    "title": "#d8e8df",
    "body": "#7a8a85",
    "holder": "#7cf0a8",
}

# Unearned / locked preview — clearly not a claimable embed.
_LOCKED = {
    "bg": "#0b0f0d",
    "stroke": "#1a2220",
    "accent": "#2a3330",
    "icon_bg": "#121816",
    "icon_stroke": "#24302c",
    "icon": "#4a5a52",
    "title": "#8a9a90",
    "body": "#5a6a62",
    "holder": "#5a6a62",
    "status": "#9a8a4a",
}


def render_achievement_badge_svg(
    badge,
    *,
    holder_handle: str | None = None,
    locked: bool = False,
) -> str:
    """Return an SVG chip with full description — wraps instead of cropping.

    ``locked=True`` is the on-site preview for viewers who have not earned the
    badge. Public embed URLs should use the unlocked art; personal proof uses
    ``holder_handle``.
    """
    if locked and holder_handle:
        raise ValueError("holder_handle is incompatible with locked=True")

    palette = _LOCKED if locked else _EARNED
    icon = xml_escape(badge.icon or "★")[:4]
    title_raw = (badge.title or "").strip()
    category_raw = badge.get_category_display()
    desc_raw = (badge.description or "").strip()
    holder_raw = f"@{holder_handle}" if holder_handle else ""
    status_raw = "locked · not earned yet" if locked else ""

    width = _MAX_WIDTH
    title_lines = wrap_words(
        title_raw,
        max_width=_TITLE_MAX_PX,
        font_size=_TITLE_SIZE,
    ) or [title_raw]

    y = 28
    title_block = tspan_lines(
        title_lines,
        x=_PAD_LEFT,
        start_y=y,
        line_height=_TITLE_LINE_H,
        fill=palette["title"],
        font_size=_TITLE_SIZE,
        font_weight="700",
    )
    y += len(title_lines) * _TITLE_LINE_H + 2

    if holder_handle:
        body_lines = wrap_words(
            category_raw,
            max_width=_BODY_MAX_PX,
            font_size=_BODY_SIZE,
        ) or [category_raw]
        holder_lines = wrap_words(
            holder_raw,
            max_width=_BODY_MAX_PX,
            font_size=_BODY_SIZE,
        ) or [holder_raw]
        body_block = tspan_lines(
            body_lines,
            x=_PAD_LEFT,
            start_y=y,
            line_height=_LINE_H,
            fill=palette["body"],
            font_size=_BODY_SIZE,
        )
        y += len(body_lines) * _LINE_H
        holder_block = tspan_lines(
            holder_lines,
            x=_PAD_LEFT,
            start_y=y,
            line_height=_LINE_H,
            fill=palette["holder"],
            font_size=_BODY_SIZE,
        )
        extra = f"  {body_block}\n  {holder_block}"
        last_baseline = y + (len(holder_lines) - 1) * _LINE_H
    elif locked:
        body_lines = wrap_words(
            desc_raw,
            max_width=_BODY_MAX_PX,
            font_size=_BODY_SIZE,
        ) or [desc_raw]
        status_lines = wrap_words(
            status_raw,
            max_width=_BODY_MAX_PX,
            font_size=_BODY_SIZE,
        ) or [status_raw]
        body_block = tspan_lines(
            body_lines,
            x=_PAD_LEFT,
            start_y=y,
            line_height=_LINE_H,
            fill=palette["body"],
            font_size=_BODY_SIZE,
        )
        y += len(body_lines) * _LINE_H + 2
        status_block = tspan_lines(
            status_lines,
            x=_PAD_LEFT,
            start_y=y,
            line_height=_LINE_H,
            fill=palette["status"],
            font_size=_BODY_SIZE,
        )
        extra = f"  {body_block}\n  {status_block}"
        last_baseline = y + (len(status_lines) - 1) * _LINE_H
    else:
        body_lines = wrap_words(
            desc_raw,
            max_width=_BODY_MAX_PX,
            font_size=_BODY_SIZE,
        ) or [desc_raw]
        body_block = tspan_lines(
            body_lines,
            x=_PAD_LEFT,
            start_y=y,
            line_height=_LINE_H,
            fill=palette["body"],
            font_size=_BODY_SIZE,
        )
        extra = f"  {body_block}"
        last_baseline = y + (len(body_lines) - 1) * _LINE_H

    height = max(72, int(last_baseline + _BODY_SIZE + 14))

    aria_title = xml_escape(title_raw) or "Badge"
    if holder_handle:
        aria = f"{aria_title} earned by @{xml_escape(holder_handle)} on DevResurge"
    elif locked:
        aria = f"{aria_title} badge locked on DevResurge — not earned yet"
    else:
        aria = f"{aria_title} badge on DevResurge"

    icon_cy = min(height / 2, 40)
    title_suffix = " (locked)" if locked else ""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{aria}">
  <title>{aria_title}{title_suffix} — DevResurge</title>
  <rect width="100%" height="100%" rx="10" fill="{palette["bg"]}" stroke="{palette["stroke"]}"/>
  <rect x="0" y="0" width="6" height="100%" fill="{palette["accent"]}"/>
  <circle cx="34" cy="{icon_cy}" r="16" fill="{palette["icon_bg"]}" stroke="{palette["icon_stroke"]}"/>
  <text x="34" y="{icon_cy + 5}" text-anchor="middle" fill="{palette["icon"]}" font-size="14"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">{icon}</text>
  {title_block}
{extra}
</svg>
"""

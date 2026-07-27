"""SVG profile badge + README export helpers."""

from __future__ import annotations

from devresurge.svg_text import tspan_lines
from devresurge.svg_text import wrap_words
from devresurge.svg_text import xml_escape

_MAX_WIDTH = 420
_PAD_LEFT = 18
_PAD_RIGHT = 18
_HIRE_CHIP_W = 96
_LINE_H = 16
_NAME_SIZE = 15
_HANDLE_SIZE = 12
_BODY_SIZE = 12
_CONTENT_W = _MAX_WIDTH - _PAD_LEFT - _PAD_RIGHT
_BODY_MAX_PX = _CONTENT_W - 8


def render_profile_badge_svg(profile, *, height: int | None = None) -> str:
    """Return a profile SVG with full role + every skill, wrapped not cropped."""
    name_raw = (profile.display_name or profile.handle or "").strip()
    handle_raw = f"@{profile.handle}"
    role_raw = profile.get_primary_role_display()
    skills = list(profile.tech_stack_list)
    stack_raw = ", ".join(skills)
    hire = bool(profile.available_for_hire)

    width = _MAX_WIDTH
    # Full content width for wrapping; hire chip gets its own top row.
    name_lines = wrap_words(
        name_raw,
        max_width=_BODY_MAX_PX,
        font_size=_NAME_SIZE,
    ) or [name_raw]
    handle_lines = wrap_words(
        handle_raw,
        max_width=_BODY_MAX_PX,
        font_size=_HANDLE_SIZE,
    ) or [handle_raw]
    role_lines = wrap_words(
        role_raw,
        max_width=_BODY_MAX_PX,
        font_size=_BODY_SIZE,
    ) or [role_raw]
    stack_lines = (
        wrap_words(stack_raw, max_width=_BODY_MAX_PX, font_size=_BODY_SIZE)
        if stack_raw
        else []
    )

    y = 28
    hire_chip = ""
    if hire:
        # Dedicated top row so the chip never covers wrapped name text.
        chip_x = width - _PAD_RIGHT - _HIRE_CHIP_W
        hire_chip = (
            f'<rect x="{chip_x}" y="12" width="{_HIRE_CHIP_W}" height="20" rx="4" fill="#1f3d2a"/>'
            f'<text x="{chip_x + _HIRE_CHIP_W / 2}" y="26" text-anchor="middle" fill="#7cf0a8" '
            f'font-size="10" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">'
            f"open to work</text>"
        )
        y = 48

    name_block = tspan_lines(
        name_lines,
        x=_PAD_LEFT,
        start_y=y,
        line_height=_LINE_H + 2,
        fill="#d8e8df",
        font_size=_NAME_SIZE,
        font_weight="700",
    )
    y += len(name_lines) * (_LINE_H + 2)

    handle_block = tspan_lines(
        handle_lines,
        x=_PAD_LEFT,
        start_y=y,
        line_height=_LINE_H,
        fill="#7cf0a8",
        font_size=_HANDLE_SIZE,
    )
    y += len(handle_lines) * _LINE_H + 2

    role_block = tspan_lines(
        role_lines,
        x=_PAD_LEFT,
        start_y=y,
        line_height=_LINE_H,
        fill="#7a8a85",
        font_size=_BODY_SIZE,
    )
    y += len(role_lines) * _LINE_H + 2

    stack_block = ""
    if stack_lines:
        stack_block = tspan_lines(
            stack_lines,
            x=_PAD_LEFT,
            start_y=y,
            line_height=_LINE_H,
            fill="#7a8a85",
            font_size=_BODY_SIZE,
        )
        last_y = y + (len(stack_lines) - 1) * _LINE_H
    else:
        last_y = y - 2 - _LINE_H  # last role baseline

    canvas_h = max(96 if height is None else height, int(last_y + _BODY_SIZE + 14))

    aria_name = xml_escape(name_raw) or "Profile"

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{canvas_h}" viewBox="0 0 {width} {canvas_h}" role="img" aria-label="{aria_name} on DevResurge">
  <title>{aria_name} — DevResurge</title>
  <rect width="100%" height="100%" rx="10" fill="#0b0f0d" stroke="#1f2c30"/>
  <rect x="0" y="0" width="6" height="100%" fill="#7cf0a8"/>
  {name_block}
  {handle_block}
  {role_block}
  {stack_block}
  {hire_chip}
</svg>
"""

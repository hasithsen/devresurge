"""SVG profile badge + README export helpers."""

from __future__ import annotations

from devresurge.svg_text import fit_canvas_width
from devresurge.svg_text import fit_single_line
from devresurge.svg_text import text_width
from devresurge.svg_text import tspan_lines
from devresurge.svg_text import wrap_words
from devresurge.svg_text import xml_escape

_MIN_WIDTH = 400
_MAX_WIDTH = 800
_PAD_LEFT = 18
_PAD_RIGHT = 18
_HIRE_CHIP_W = 96
_HIRE_GAP = 14
_LINE_H = 15
_NAME_SIZE = 15
_HANDLE_SIZE = 12
_BODY_SIZE = 11


def render_profile_badge_svg(profile, *, height: int | None = None) -> str:
    """Return a shields-style SVG badge with full name/role and all skills."""
    name_raw = (profile.display_name or profile.handle or "").strip()
    handle_raw = f"@{profile.handle}"
    role_raw = profile.get_primary_role_display()
    skills = list(profile.tech_stack_list)
    stack_raw = ", ".join(skills)
    hire = bool(profile.available_for_hire)

    hire_reserve = (_HIRE_CHIP_W + _HIRE_GAP) if hire else 0

    # Size for the longest single-line field; skills wrap fully below.
    width = fit_canvas_width(
        text_width(name_raw, _NAME_SIZE) + hire_reserve,
        text_width(handle_raw, _HANDLE_SIZE),
        text_width(role_raw, _BODY_SIZE),
        # Comfortable skill column so typical stacks wrap cleanly.
        420 + hire_reserve,
        pad_left=_PAD_LEFT,
        pad_right=_PAD_RIGHT,
        min_width=_MIN_WIDTH,
        max_width=_MAX_WIDTH,
    )

    name_max = width - _PAD_LEFT - _PAD_RIGHT - hire_reserve
    line_max = width - _PAD_LEFT - _PAD_RIGHT

    name = fit_single_line(name_raw, max_width=name_max, font_size=_NAME_SIZE)
    handle = fit_single_line(handle_raw, max_width=line_max, font_size=_HANDLE_SIZE)
    role_lines = wrap_words(
        role_raw,
        max_width=line_max,
        font_size=_BODY_SIZE,
        max_lines=None,
    ) or [role_raw]
    stack_lines = (
        wrap_words(
            stack_raw,
            max_width=line_max,
            font_size=_BODY_SIZE,
            max_lines=None,  # every skill, no ellipsis
        )
        if stack_raw
        else []
    )

    y_role = 66
    role_block = tspan_lines(
        role_lines,
        x=_PAD_LEFT,
        start_y=y_role,
        line_height=_LINE_H,
        fill="#7a8a85",
        font_size=_BODY_SIZE,
    )

    stack_block = ""
    stack_start = y_role + len(role_lines) * _LINE_H + 2
    if stack_lines:
        stack_block = tspan_lines(
            stack_lines,
            x=_PAD_LEFT,
            start_y=stack_start,
            line_height=_LINE_H,
            fill="#7a8a85",
            font_size=_BODY_SIZE,
        )
        last_y = stack_start + (len(stack_lines) - 1) * _LINE_H
    else:
        last_y = y_role + (len(role_lines) - 1) * _LINE_H

    canvas_h = max(96 if height is None else height, int(last_y + 18))

    hire_chip = ""
    if hire:
        chip_x = width - _PAD_RIGHT - _HIRE_CHIP_W
        hire_chip = (
            f'<rect x="{chip_x}" y="14" width="{_HIRE_CHIP_W}" height="20" rx="4" fill="#1f3d2a"/>'
            f'<text x="{chip_x + _HIRE_CHIP_W / 2}" y="28" text-anchor="middle" fill="#7cf0a8" '
            f'font-size="10" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">'
            f"open to work</text>"
        )

    aria_name = xml_escape(name_raw) or "Profile"

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{canvas_h}" viewBox="0 0 {width} {canvas_h}" role="img" aria-label="{aria_name} on DevResurge">
  <title>{aria_name} — DevResurge</title>
  <rect width="100%" height="100%" rx="10" fill="#0b0f0d" stroke="#1f2c30"/>
  <rect x="0" y="0" width="6" height="100%" fill="#7cf0a8"/>
  <text x="{_PAD_LEFT}" y="28" fill="#d8e8df" font-size="{_NAME_SIZE}" font-weight="700"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">{name}</text>
  <text x="{_PAD_LEFT}" y="48" fill="#7cf0a8" font-size="{_HANDLE_SIZE}"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">{handle}</text>
  {role_block}
  {stack_block}
  {hire_chip}
</svg>
"""

"""SVG profile badge + README export helpers."""

from __future__ import annotations

from devresurge.svg_text import fit_canvas_width
from devresurge.svg_text import fit_single_line
from devresurge.svg_text import text_width
from devresurge.svg_text import tspan_lines
from devresurge.svg_text import wrap_words
from devresurge.svg_text import xml_escape

_MIN_WIDTH = 380
_MAX_WIDTH = 720
_PAD_LEFT = 18
_PAD_RIGHT = 18
_HIRE_CHIP_W = 96
_HIRE_GAP = 14
_LINE_H = 14


def render_profile_badge_svg(profile, *, height: int | None = None) -> str:
    """Return a shields-style SVG badge sized so profile text never clips."""
    name_raw = (profile.display_name or profile.handle or "").strip()
    handle_raw = f"@{profile.handle}"
    role_raw = profile.get_primary_role_display()
    stack_raw = ", ".join(profile.tech_stack_list[:4])
    hire = bool(profile.available_for_hire)

    hire_reserve = (_HIRE_CHIP_W + _HIRE_GAP) if hire else 0
    target_line = 360

    width = fit_canvas_width(
        text_width(name_raw, 15) + hire_reserve,
        text_width(handle_raw, 12),
        text_width(role_raw, 11),
        text_width(stack_raw, 11) if stack_raw else 0,
        target_line + hire_reserve,
        pad_left=_PAD_LEFT,
        pad_right=_PAD_RIGHT,
        min_width=_MIN_WIDTH,
        max_width=_MAX_WIDTH,
    )

    name_max = width - _PAD_LEFT - _PAD_RIGHT - hire_reserve
    line_max = width - _PAD_LEFT - _PAD_RIGHT

    name = fit_single_line(name_raw, max_width=name_max, font_size=15)
    handle = fit_single_line(handle_raw, max_width=line_max, font_size=12)
    role_lines = wrap_words(role_raw, max_width=line_max, font_size=11, max_lines=1)
    stack_lines = (
        wrap_words(stack_raw, max_width=line_max, font_size=11, max_lines=2)
        if stack_raw
        else []
    )

    # Layout: name 28, handle 48, role 66, stack starts 82 (may wrap).
    role_block = tspan_lines(
        role_lines,
        x=_PAD_LEFT,
        start_y=66,
        line_height=_LINE_H,
        fill="#7a8a85",
        font_size=11,
    )
    stack_block = ""
    stack_start = 82
    if stack_lines:
        stack_block = tspan_lines(
            stack_lines,
            x=_PAD_LEFT,
            start_y=stack_start,
            line_height=_LINE_H,
            fill="#7a8a85",
            font_size=11,
        )
        canvas_h = stack_start + (len(stack_lines) - 1) * _LINE_H + 16
    else:
        canvas_h = 78
    canvas_h = max(96 if height is None else height, canvas_h)

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
  <text x="{_PAD_LEFT}" y="28" fill="#d8e8df" font-size="15" font-weight="700"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">{name}</text>
  <text x="{_PAD_LEFT}" y="48" fill="#7cf0a8" font-size="12"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">{handle}</text>
  {role_block}
  {stack_block}
  {hire_chip}
</svg>
"""

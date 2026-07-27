"""SVG profile badge + README export helpers."""

from __future__ import annotations

import html
import re

_XML_SAFE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")

_MONO_ADVANCE = 0.62
_MIN_WIDTH = 360
_MAX_WIDTH = 640
_PAD_LEFT = 18
_PAD_RIGHT = 18
_HIRE_CHIP_W = 96
_HIRE_GAP = 12


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


def render_profile_badge_svg(profile, *, height: int = 96) -> str:
    """Return a shields-style SVG badge sized to fit profile text without clipping."""
    name_raw = (profile.display_name or profile.handle or "").strip()
    handle_raw = f"@{profile.handle}"
    role_raw = profile.get_primary_role_display()
    stack_raw = ", ".join(profile.tech_stack_list[:4])
    hire = bool(profile.available_for_hire)

    name_w = _text_width(name_raw, 15)
    handle_w = _text_width(handle_raw, 12)
    role_w = _text_width(role_raw, 11)
    stack_w = _text_width(stack_raw, 11) if stack_raw else 0

    # Name row shares space with the hire chip when present.
    name_row = name_w + ((_HIRE_CHIP_W + _HIRE_GAP) if hire else 0)
    content_w = max(name_row, handle_w, role_w, stack_w, 280)
    width = int(min(_MAX_WIDTH, max(_MIN_WIDTH, _PAD_LEFT + content_w + _PAD_RIGHT)))

    hire_reserve = (_HIRE_CHIP_W + _HIRE_GAP) if hire else 0
    name_max = width - _PAD_LEFT - _PAD_RIGHT - hire_reserve
    line_max = width - _PAD_LEFT - _PAD_RIGHT

    name = _fit_text(name_raw, max_width=name_max, font_size=15)
    handle = _fit_text(handle_raw, max_width=line_max, font_size=12)
    role = _fit_text(role_raw, max_width=line_max, font_size=11)
    stack_line = (
        _fit_text(stack_raw, max_width=line_max, font_size=11) if stack_raw else ""
    )

    hire_chip = ""
    if hire:
        chip_x = width - _PAD_RIGHT - _HIRE_CHIP_W
        hire_chip = (
            f'<rect x="{chip_x}" y="14" width="{_HIRE_CHIP_W}" height="20" rx="4" fill="#1f3d2a"/>'
            f'<text x="{chip_x + _HIRE_CHIP_W / 2}" y="28" text-anchor="middle" fill="#7cf0a8" '
            f'font-size="10" font-family="ui-monospace, SFMono-Regular, Menlo, monospace">'
            f"open to work</text>"
        )

    stack_svg = ""
    if stack_line:
        stack_svg = (
            f'<text x="{_PAD_LEFT}" y="78" fill="#7a8a85" font-size="11" '
            f'font-family="ui-monospace, SFMono-Regular, Menlo, monospace">'
            f"{stack_line}</text>"
        )

    aria_name = _xml_escape(name_raw) or "Profile"

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{aria_name} on DevResurge">
  <title>{aria_name} — DevResurge</title>
  <rect width="100%" height="100%" rx="10" fill="#0b0f0d" stroke="#1f2c30"/>
  <rect x="0" y="0" width="6" height="100%" fill="#7cf0a8"/>
  <text x="{_PAD_LEFT}" y="28" fill="#d8e8df" font-size="15" font-weight="700"
        font-family="ui-monospace, SFMono-Regular, Menlo, monospace">{name}</text>
  <text x="{_PAD_LEFT}" y="48" fill="#7cf0a8" font-size="12"
        font-family="ui-monospace, SFMono-Regular, Menlo, monospace">{handle}</text>
  <text x="{_PAD_LEFT}" y="66" fill="#7a8a85" font-size="11"
        font-family="ui-monospace, SFMono-Regular, Menlo, monospace">{role}</text>
  {stack_svg}
  {hire_chip}
</svg>
"""

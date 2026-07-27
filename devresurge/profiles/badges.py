"""SVG profile badge + README export helpers."""

from __future__ import annotations

import html
import re

_XML_SAFE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def _xml_text(value: str, *, limit: int = 80) -> str:
    cleaned = _XML_SAFE.sub("", (value or "").strip())[:limit]
    return html.escape(cleaned, quote=False)


def render_profile_badge_svg(profile, *, width: int = 420, height: int = 96) -> str:
    """Return a shields-style SVG badge for embedding in READMEs / sites."""
    name = _xml_text(profile.display_name or profile.handle, limit=36)
    handle = _xml_text(f"@{profile.handle}", limit=32)
    role = _xml_text(profile.get_primary_role_display(), limit=40)
    stack = ", ".join(profile.tech_stack_list[:4])
    stack_line = _xml_text(stack, limit=48) if stack else ""
    hire = profile.available_for_hire

    hire_chip = ""
    if hire:
        hire_chip = (
            '<rect x="320" y="14" width="86" height="20" rx="4" fill="#1f3d2a"/>'
            '<text x="363" y="28" text-anchor="middle" fill="#7cf0a8" '
            'font-size="10" font-family="ui-monospace, SFMono-Regular, Menlo, monospace">'
            "open to work</text>"
        )

    stack_svg = ""
    if stack_line:
        stack_svg = (
            f'<text x="18" y="78" fill="#7a8a85" font-size="11" '
            f'font-family="ui-monospace, SFMono-Regular, Menlo, monospace">'
            f"{stack_line}</text>"
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" role="img" aria-label="{name} on DevResurge">
  <title>{name} — DevResurge</title>
  <rect width="100%" height="100%" rx="10" fill="#0b0f0d" stroke="#1f2c30"/>
  <rect x="0" y="0" width="6" height="100%" fill="#7cf0a8"/>
  <text x="18" y="28" fill="#d8e8df" font-size="15" font-weight="700"
        font-family="ui-monospace, SFMono-Regular, Menlo, monospace">{name}</text>
  <text x="18" y="48" fill="#7cf0a8" font-size="12"
        font-family="ui-monospace, SFMono-Regular, Menlo, monospace">{handle}</text>
  <text x="18" y="66" fill="#7a8a85" font-size="11"
        font-family="ui-monospace, SFMono-Regular, Menlo, monospace">{role}</text>
  {stack_svg}
  {hire_chip}
</svg>
"""

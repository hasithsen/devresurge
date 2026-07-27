"""Shared SVG text measurement helpers for embeddable badges.

Glyph widths are intentionally overestimated so text never clips when the SVG
is rasterized as ``<img>`` (overflow is hidden in that context).
"""

from __future__ import annotations

import html
import math
import re

_XML_SAFE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")

# Conservative monospace advance (em). Real SFMono/Menlo sit near ~0.6;
# we pad so fallback fonts and bold weights never overflow the canvas.
_MONO_ADVANCE = 0.72
_SAFETY_PX = 14


def clean_text(value: str) -> str:
    return _XML_SAFE.sub("", (value or "").strip())


def xml_escape(value: str) -> str:
    return html.escape(clean_text(value), quote=False)


def text_width(text: str, font_size: float) -> float:
    return len(text) * font_size * _MONO_ADVANCE


def fit_canvas_width(
    *widths: float,
    pad_left: float,
    pad_right: float,
    min_width: int,
    max_width: int,
) -> int:
    """Ceil + safety padding so measured text always fits inside the SVG."""
    content = max(widths) if widths else 0
    needed = math.ceil(pad_left + content + pad_right + _SAFETY_PX)
    return int(min(max_width, max(min_width, needed)))


def _ellipsis(raw: str, *, max_width: float, font_size: float) -> str:
    cleaned = clean_text(raw)
    if not cleaned or text_width(cleaned, font_size) <= max_width:
        return cleaned
    ellipsis = "…"
    budget = max_width - text_width(ellipsis, font_size)
    if budget <= 0:
        return ellipsis
    lo, hi = 0, len(cleaned)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if text_width(cleaned[:mid], font_size) <= budget:
            lo = mid
        else:
            hi = mid - 1
    cut = cleaned[:lo].rstrip()
    if " " in cut and len(cut) > 8:
        cut = cut.rsplit(" ", 1)[0]
    return f"{cut}{ellipsis}"


def wrap_words(
    raw: str,
    *,
    max_width: float,
    font_size: float,
    max_lines: int = 2,
) -> list[str]:
    """Word-wrap ``raw`` into up to ``max_lines`` lines that fit ``max_width``."""
    cleaned = clean_text(raw)
    if not cleaned:
        return []
    if text_width(cleaned, font_size) <= max_width:
        return [cleaned]
    if max_lines <= 1:
        return [_ellipsis(cleaned, max_width=max_width, font_size=font_size)]

    words = cleaned.split()
    if not words:
        return [cleaned]

    lines: list[str] = []
    current = ""
    i = 0
    while i < len(words):
        word = words[i]
        candidate = word if not current else f"{current} {word}"
        if text_width(candidate, font_size) <= max_width:
            current = candidate
            i += 1
            continue

        if not current:
            lines.append(_ellipsis(word, max_width=max_width, font_size=font_size))
            i += 1
        else:
            lines.append(current)
            current = ""

        remaining_slots = max_lines - len(lines)
        if remaining_slots <= 1:
            rest = " ".join(([current] if current else []) + words[i:])
            lines.append(_ellipsis(rest, max_width=max_width, font_size=font_size))
            return lines[:max_lines]

    if current:
        lines.append(current)
    return lines[:max_lines]


def fit_single_line(raw: str, *, max_width: float, font_size: float) -> str:
    """Escape a single line, ellipsizing only when it cannot fit."""
    return xml_escape(_ellipsis(raw, max_width=max_width, font_size=font_size))


def tspan_lines(
    lines: list[str],
    *,
    x: float,
    start_y: float,
    line_height: float,
    fill: str,
    font_size: float,
    font_weight: str = "400",
) -> str:
    """Render wrapped lines as absolute-positioned ``<text>`` elements."""
    weight_attr = f' font-weight="{font_weight}"' if font_weight != "400" else ""
    parts = []
    for i, line in enumerate(lines):
        y = start_y + i * line_height
        parts.append(
            f'<text x="{x}" y="{y}" fill="{fill}" font-size="{font_size}"{weight_attr} '
            f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">'
            f"{xml_escape(line)}</text>",
        )
    return "\n  ".join(parts)
